#!/usr/bin/env python
# coding: utf-8
"""
Email templates for authentication system.
"""


def get_verification_email_template(verification_url: str) -> str:
    """
    Get HTML template for email verification.
    
    Args:
        verification_url (str): URL with verification token
    
    Returns:
        str: HTML email template
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                padding: 30px;
                border-radius: 10px;
                border: 1px solid #ddd;
            }}
            .header {{
                text-align: center;
                color: #2c3e50;
                margin-bottom: 30px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="header">Verify Your Email Address</h1>
            <p>Thank you for signing up for Multi-Agent Stock Analyst!</p>
            <p>Please click the button below to verify your email address and complete your registration:</p>
            <div style="text-align: center;">
                <a href="{verification_url}" class="button">Verify Email</a>
            </div>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #666;">{verification_url}</p>
            <p><strong>This link will expire in 24 hours.</strong></p>
            <div class="footer">
                <p>If you did not sign up for this account, please ignore this email.</p>
                <p>© Multi-Agent Stock Analyst</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_password_reset_email_template(reset_url: str) -> str:
    """
    Get HTML template for password reset.
    
    Args:
        reset_url (str): URL with reset token
    
    Returns:
        str: HTML email template
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                padding: 30px;
                border-radius: 10px;
                border: 1px solid #ddd;
            }}
            .header {{
                text-align: center;
                color: #2c3e50;
                margin-bottom: 30px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background-color: #e74c3c;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #777;
                text-align: center;
            }}
            .warning {{
                background-color: #fff3cd;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #ffc107;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="header">Reset Your Password</h1>
            <p>We received a request to reset your password for your Multi-Agent Stock Analyst account.</p>
            <p>Click the button below to reset your password:</p>
            <div style="text-align: center;">
                <a href="{reset_url}" class="button">Reset Password</a>
            </div>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #666;">{reset_url}</p>
            <div class="warning">
                <p><strong>Important:</strong> This link will expire in 1 hour.</p>
                <p>If you did not request a password reset, please ignore this email. Your password will remain unchanged.</p>
            </div>
            <div class="footer">
                <p>© Multi-Agent Stock Analyst</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_admin_notification_template(user_email: str) -> str:
    """
    Get HTML template for admin notification email.
    
    Args:
        user_email (str): Email of the newly registered user
    
    Returns:
        str: HTML email template
    """
    from datetime import datetime
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                padding: 30px;
                border-radius: 10px;
                border: 1px solid #ddd;
            }}
            .header {{
                text-align: center;
                color: #2c3e50;
                margin-bottom: 30px;
            }}
            .info-box {{
                background-color: #e8f4f8;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #3498db;
                margin: 20px 0;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="header">New User Registration</h1>
            <p>A new user has registered for Multi-Agent Stock Analyst.</p>
            <div class="info-box">
                <p><strong>User Email:</strong> {user_email}</p>
                <p><strong>Registration Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            <p>Please review the user registration in the admin panel.</p>
            <div class="footer">
                <p>© Multi-Agent Stock Analyst - Admin Notification</p>
            </div>
        </div>
    </body>
    </html>
    """

