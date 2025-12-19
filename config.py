#!/usr/bin/env python
# coding: utf-8
"""
Configuration module for authentication system.

SMTP settings can be configured via environment variables or by modifying
the default values in this file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# SMTP Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USERNAME)

# Admin email for notifications
ADMIN_EMAIL = "dinesh.katiyar@trustassist.ai"

# Application URL (for email links)
# Priority: APP_BASE_URL (for Cloud Run) > APP_URL > localhost default
APP_BASE_URL = os.getenv("APP_BASE_URL", os.getenv("APP_URL", "http://localhost:8501"))
APP_URL = APP_BASE_URL  # Keep for backward compatibility

# Token expiration times (in hours)
VERIFICATION_TOKEN_EXPIRY_HOURS = 24
PASSWORD_RESET_TOKEN_EXPIRY_HOURS = 1

# Database file
DATABASE_FILE = "auth.db"

