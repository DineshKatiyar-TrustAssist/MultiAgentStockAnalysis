#!/usr/bin/env python
# coding: utf-8
"""
Email Verification page for completing user registration.
"""

import streamlit as st
import sys
from pathlib import Path
from urllib.parse import unquote

# Add parent directory to path to import auth module
sys.path.insert(0, str(Path(__file__).parent.parent))

import auth
from auth import AuthError

st.set_page_config(
    page_title="Verify Email - Multi-Agent Stock Analyst",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Modern CSS styling
st.markdown("""
<style>
    /* Hide sidebar navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Page background */
    .stApp {
        background-color: #f3f4f6;
        min-height: 100vh;
    }

    /* Main container */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 420px;
    }

    /* Remove top padding */
    .block-container {
        padding-top: 1rem !important;
    }

    /* Hide empty Streamlit elements */
    .element-container:has(> div:empty),
    .stMarkdown:empty,
    div:empty:not([class]) {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Card styling */
    .auth-card {
        background: white;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        padding: 1.5rem 2rem;
        width: fit-content;
        max-width: 100%;
        margin: 0 auto 2rem auto;
    }

    /* Logo/Icon area */
    .auth-logo {
        text-align: center;
        margin-bottom: 0.75rem;
    }

    .auth-logo .icon {
        font-size: 2rem;
        color: #667eea;
    }

    /* Title styling */
    .auth-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.25rem;
        text-align: center;
        letter-spacing: -0.5px;
    }

    /* Subtitle styling */
    .auth-subtitle {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 1rem;
        text-align: center;
    }

    /* User email display */
    .user-email {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 4px;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        text-align: center;
        font-size: 0.85rem;
        color: #374151;
    }

    .user-email strong {
        color: #667eea;
    }

    /* Form input styling */
    .stTextInput > div > div > input {
        border-radius: 4px;
        border: 1px solid #d1d5db;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        background-color: white;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        outline: none;
        background-color: white;
    }

    .stTextInput > div > div > input::placeholder {
        color: #9ca3af;
    }

    /* Label styling */
    .stTextInput label {
        font-weight: 600;
        color: #374151;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }

    /* Primary button */
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button {
        width: 100%;
        border-radius: 4px;
        padding: 0.75rem 1.25rem;
        font-weight: 500;
        font-size: 0.95rem;
        border: 1px solid #10b981;
        background: #10b981;
        color: white;
    }

    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {
        background: #059669;
        border-color: #059669;
    }

    /* Secondary button */
    .stButton > button:not([kind="primary"]) {
        width: 100%;
        border-radius: 4px;
        padding: 0.65rem 1.25rem;
        font-weight: 500;
        font-size: 0.9rem;
        background: white;
        color: #667eea;
        border: 1px solid #d1d5db;
    }

    .stButton > button:not([kind="primary"]):hover {
        border-color: #667eea;
        background: #f9fafb;
    }

    /* Error state card */
    .error-icon {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }

    /* Success/Error messages */
    .stAlert {
        border-radius: 4px;
    }

    /* Password requirements */
    .password-hint {
        font-size: 0.8rem;
        color: #6b7280;
        margin-top: -0.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* Form spacing */
    .stForm {
        margin-bottom: 0.75rem;
    }
    
    .stForm > div {
        margin-bottom: 0.5rem;
    }
    
    /* Reduce spacing between form elements */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Get token from URL query parameters
query_params = st.query_params
token = query_params.get("token", "")

# URL decode the token to handle special characters
if token:
    token = unquote(token)

# Main card container
if not token:
    # No token provided
    st.markdown('''<div class="auth-card">
        <div class="auth-logo"><span class="error-icon">🔗</span></div>
        <h1 class="auth-title">Invalid Link</h1>
        <p class="auth-subtitle">No verification token was provided</p>
    ''', unsafe_allow_html=True)

    st.error("Please use the verification link from your email.")

    if st.button("Go to Sign Up", use_container_width=True):
        st.switch_page("pages/signup.py")
else:
    # Verify the token
    user_id = auth.verify_email_token(token)

    if not user_id:
        # Invalid or expired token
        st.markdown('''<div class="auth-card">
            <div class="auth-logo"><span class="error-icon">⏰</span></div>
            <h1 class="auth-title">Link Expired</h1>
            <p class="auth-subtitle">This verification link is no longer valid</p>
        ''', unsafe_allow_html=True)

        st.warning("Verification links expire after 24 hours or after being used.")

        if st.button("Sign Up Again", use_container_width=True):
            st.switch_page("pages/signup.py")
    else:
        # Valid token - get user info
        user = auth.get_user_by_id(user_id)

        if user and user.get('is_verified'):
            # User already verified
            st.markdown('''<div class="auth-card">
                <div class="auth-logo"><span class="icon">✅</span></div>
                <h1 class="auth-title">Already Verified</h1>
                <p class="auth-subtitle">Your email has been verified</p>
            ''', unsafe_allow_html=True)

            st.success("You can now sign in to your account.")

            if st.button("Sign In", use_container_width=True):
                st.switch_page("pages/signin.py")
        else:
            # Show password creation form
            user_email_html = f'<div class="user-email">Setting up account for <strong>{user["email"]}</strong></div>' if user else ''
            st.markdown(f'''<div class="auth-card">
                <div class="auth-logo"><span class="icon">🔐</span></div>
                <h1 class="auth-title">Set Your Password</h1>
                <p class="auth-subtitle">Create a secure password for your account</p>
                {user_email_html}
            ''', unsafe_allow_html=True)

            with st.form("set_password_form", clear_on_submit=False):
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a strong password"
                )
                st.markdown('<p class="password-hint">Must be at least 8 characters</p>', unsafe_allow_html=True)

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password"
                )

                submit_button = st.form_submit_button("Complete Setup", type="primary", use_container_width=True)

            if submit_button:
                if not password or not confirm_password:
                    st.error("Please fill in both password fields")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters long")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    try:
                        with st.spinner("Setting up your account..."):
                            auth.set_password(user_id, password)

                            # Auto-login the user
                            st.session_state.authenticated = True
                            st.session_state.user_id = user_id
                            st.session_state.user_email = user['email']

                            st.success("Account setup complete!")
                            st.switch_page("app.py")
                    except AuthError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)
