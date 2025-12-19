#!/usr/bin/env python
# coding: utf-8
"""
Authentication module for Multi-Agent Stock Analyst.

Handles user registration, email verification, password management,
and session management.
"""

import sqlite3
import secrets
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from urllib.parse import quote
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
from email_templates import (
    get_verification_email_template,
    get_password_reset_email_template,
    get_admin_notification_template
)


class AuthError(Exception):
    """Custom exception for authentication errors."""
    pass


def get_db_connection():
    """
    Get a database connection.

    Returns:
        sqlite3.Connection: Database connection
    """
    conn = sqlite3.connect(config.DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """
    Initialize the database with required tables.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            is_verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create email_verification_tokens table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_verification_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Create password_reset_tokens table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_verification_token ON email_verification_tokens(token)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reset_token ON password_reset_tokens(token)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_email ON users(email)")

    conn.commit()
    conn.close()


def validate_email_format(email: str) -> bool:
    """
    Validate email format.

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): Plain text password

    Returns:
        str: Hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        password (str): Plain text password
        password_hash (str): Hashed password

    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def generate_secure_token() -> str:
    """
    Generate a secure random token.

    Returns:
        str: URL-safe token
    """
    return secrets.token_urlsafe(32)


def send_email(to_email: str, subject: str, html_body: str) -> bool:
    """
    Send an email using SMTP.

    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        html_body (str): HTML email body

    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        if not config.SMTP_USERNAME or not config.SMTP_PASSWORD:
            raise AuthError("SMTP credentials not configured")

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = config.FROM_EMAIL
        msg['To'] = to_email

        # Add HTML body
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)

        # Send email
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def register_user(email: str) -> Tuple[int, str]:
    """
    Register a new user and send verification email.

    Args:
        email (str): User email address

    Returns:
        Tuple[int, str]: (user_id, verification_token)

    Raises:
        AuthError: If email is invalid or user already exists
    """
    # Validate email format
    if not validate_email_format(email):
        raise AuthError("Invalid email format")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email.lower(),))
        existing_user = cursor.fetchone()

        if existing_user:
            raise AuthError("User with this email already exists")

        # Create user (without password yet)
        cursor.execute("""
            INSERT INTO users (email, is_verified)
            VALUES (?, 0)
        """, (email.lower(),))

        user_id = cursor.lastrowid

        # Generate verification token
        token = generate_secure_token()
        expires_at = datetime.now() + timedelta(hours=config.VERIFICATION_TOKEN_EXPIRY_HOURS)

        cursor.execute("""
            INSERT INTO email_verification_tokens (user_id, token, expires_at)
            VALUES (?, ?, ?)
        """, (user_id, token, expires_at))

        conn.commit()

        # Send verification email
        encoded_token = quote(token, safe='')
        verification_url = f"{config.APP_BASE_URL}/verify_email?token={encoded_token}"
        email_body = get_verification_email_template(verification_url)
        send_email(email, "Verify Your Email - Multi-Agent Stock Analyst", email_body)

        # Send admin notification
        admin_body = get_admin_notification_template(email)
        send_email(config.ADMIN_EMAIL, f"New User Registration: {email}", admin_body)

        return user_id, token

    except sqlite3.IntegrityError:
        conn.rollback()
        raise AuthError("User with this email already exists")
    except AuthError:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise AuthError(f"Error creating user: {str(e)}")
    finally:
        conn.close()


def verify_email_token(token: str) -> Optional[int]:
    """
    Verify an email verification token.

    Args:
        token (str): Verification token

    Returns:
        Optional[int]: User ID if token is valid, None otherwise
    """
    if not token or not token.strip():
        return None

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT user_id, expires_at, used_at
            FROM email_verification_tokens
            WHERE token = ?
        """, (token.strip(),))

        result = cursor.fetchone()

        if not result:
            return None

        user_id, expires_at_str, used_at = result

        # Check if token already used
        if used_at:
            return None

        # Parse expires_at - handle both string and datetime objects
        if isinstance(expires_at_str, str):
            expires_at = datetime.fromisoformat(expires_at_str)
        else:
            expires_at = expires_at_str

        # Check if token is expired
        if datetime.now() > expires_at:
            return None

        return user_id

    except Exception as e:
        print(f"Error verifying token: {str(e)}")
        return None
    finally:
        conn.close()


def set_password(user_id: int, password: str) -> bool:
    """
    Set password for a user and mark as verified.

    Args:
        user_id (int): User ID
        password (str): Plain text password

    Returns:
        bool: True if successful, False otherwise
    """
    if len(password) < 8:
        raise AuthError("Password must be at least 8 characters long")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        password_hash = hash_password(password)

        cursor.execute("""
            UPDATE users
            SET password_hash = ?, is_verified = 1, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (password_hash, user_id))

        # Mark verification token as used
        cursor.execute("""
            UPDATE email_verification_tokens
            SET used_at = CURRENT_TIMESTAMP
            WHERE user_id = ? AND used_at IS NULL
        """, (user_id,))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        raise AuthError(f"Error setting password: {str(e)}")
    finally:
        conn.close()


def authenticate(email: str, password: str) -> Optional[Dict]:
    """
    Authenticate a user with email and password.

    Args:
        email (str): User email
        password (str): User password

    Returns:
        Optional[Dict]: User data if authenticated, None otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, email, password_hash, is_verified
            FROM users
            WHERE email = ?
        """, (email.lower(),))

        user = cursor.fetchone()

        if not user:
            return None

        user_id, user_email, password_hash, is_verified = user

        # Check if user is verified
        if not is_verified:
            raise AuthError("Email not verified. Please verify your email first.")

        # Check if password is set
        if not password_hash:
            raise AuthError("Password not set. Please complete registration.")

        # Verify password
        if not verify_password(password, password_hash):
            return None

        return {
            'id': user_id,
            'email': user_email,
            'is_verified': bool(is_verified)
        }

    finally:
        conn.close()


def request_password_reset(email: str) -> Optional[str]:
    """
    Create a password reset token for a user.

    Args:
        email (str): User email

    Returns:
        Optional[str]: Reset token if user exists, None otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE email = ?", (email.lower(),))
        user = cursor.fetchone()

        if not user:
            return None  # Don't reveal if user exists or not

        user_id = user[0]

        # Generate reset token
        token = generate_secure_token()
        expires_at = datetime.now() + timedelta(hours=config.PASSWORD_RESET_TOKEN_EXPIRY_HOURS)

        cursor.execute("""
            INSERT INTO password_reset_tokens (user_id, token, expires_at)
            VALUES (?, ?, ?)
        """, (user_id, token, expires_at))

        conn.commit()

        # Send reset email
        encoded_token = quote(token, safe='')
        reset_url = f"{config.APP_BASE_URL}/reset_password?token={encoded_token}"
        email_body = get_password_reset_email_template(reset_url)
        send_email(email, "Reset Your Password - Multi-Agent Stock Analyst", email_body)

        return token

    except Exception as e:
        conn.rollback()
        return None
    finally:
        conn.close()


def verify_reset_token(token: str) -> Optional[int]:
    """
    Verify a password reset token.

    Args:
        token (str): Reset token

    Returns:
        Optional[int]: User ID if token is valid, None otherwise
    """
    if not token or not token.strip():
        return None

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT user_id, expires_at, used_at
            FROM password_reset_tokens
            WHERE token = ?
        """, (token.strip(),))

        result = cursor.fetchone()

        if not result:
            return None

        user_id, expires_at_str, used_at = result

        # Check if token already used
        if used_at:
            return None

        # Parse expires_at - handle both string and datetime objects
        if isinstance(expires_at_str, str):
            expires_at = datetime.fromisoformat(expires_at_str)
        else:
            expires_at = expires_at_str

        # Check if token is expired
        if datetime.now() > expires_at:
            return None

        return user_id

    except Exception as e:
        print(f"Error verifying reset token: {str(e)}")
        return None
    finally:
        conn.close()


def reset_password(user_id: int, new_password: str) -> bool:
    """
    Reset password for a user.

    Args:
        user_id (int): User ID
        new_password (str): New plain text password

    Returns:
        bool: True if successful, False otherwise
    """
    if len(new_password) < 8:
        raise AuthError("Password must be at least 8 characters long")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        password_hash = hash_password(new_password)

        cursor.execute("""
            UPDATE users
            SET password_hash = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (password_hash, user_id))

        # Mark reset token as used
        cursor.execute("""
            UPDATE password_reset_tokens
            SET used_at = CURRENT_TIMESTAMP
            WHERE user_id = ? AND used_at IS NULL
        """, (user_id,))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        raise AuthError(f"Error resetting password: {str(e)}")
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> Optional[Dict]:
    """
    Get user by ID.

    Args:
        user_id (int): User ID

    Returns:
        Optional[Dict]: User data if found, None otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, email, is_verified
            FROM users
            WHERE id = ?
        """, (user_id,))

        user = cursor.fetchone()

        if not user:
            return None

        return {
            'id': user[0],
            'email': user[1],
            'is_verified': bool(user[2])
        }

    finally:
        conn.close()


# Initialize database on import
init_database()
