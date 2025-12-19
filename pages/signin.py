#!/usr/bin/env python
# coding: utf-8
"""
Sign In page for user authentication.
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import auth module
sys.path.insert(0, str(Path(__file__).parent.parent))

import auth
from auth import AuthError

st.set_page_config(
    page_title="Sign In - Multi-Agent Stock Analyst",
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
         display: flex;
         flex-direction: column;
         align-items: center;
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
         padding: 2rem 2.5rem;
         width: fit-content;
         max-width: 100%;
         margin: 0 auto 2rem auto;
     }


     /* Logo/Icon area */
     .auth-logo {
         text-align: center;
         margin-bottom: 1rem;
     }

     .auth-logo .icon {
         font-size: 2.5rem;
         color: #667eea;
     }

     /* Title styling */
     .auth-title {
         font-size: 1.5rem;
         font-weight: 700;
         color: #1a1a2e;
         margin-bottom: 0.5rem;
         text-align: center;
         letter-spacing: -0.5px;
     }

     /* Subtitle styling */
     .auth-subtitle {
         font-size: 0.9rem;
         color: #6b7280;
         margin-bottom: 1.5rem;
         text-align: center;
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
         border: 1px solid #667eea;
         background: #667eea;
         color: white;
     }

    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {
        background: #5568d3;
        border-color: #5568d3;
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

    /* Divider */
    .auth-divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
        color: #9ca3af;
        font-size: 0.85rem;
    }

    .auth-divider::before,
    .auth-divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #e5e7eb;
    }

    .auth-divider::before {
        margin-right: 1rem;
    }

    .auth-divider::after {
        margin-left: 1rem;
    }

    /* Link text */
    .auth-link-text {
        text-align: center;
        color: #6b7280;
        font-size: 0.95rem;
        margin-top: 1.5rem;
    }

     /* Success/Error messages */
     .stAlert {
         border-radius: 4px;
     }
     
     /* Form spacing */
     .stForm {
         margin-bottom: 1rem;
     }
     
     .stForm > div {
         margin-bottom: 0.75rem;
     }
     
     /* Reduce spacing between form elements */
     .element-container {
         margin-bottom: 0.75rem !important;
     }
 </style>
 """, unsafe_allow_html=True)

# Check if user is already authenticated
if 'authenticated' in st.session_state and st.session_state.authenticated:
    st.switch_page("app.py")

# Initialize session state for forgot password view
if 'show_forgot_password' not in st.session_state:
    st.session_state.show_forgot_password = False

# Main card container with logo
if st.session_state.show_forgot_password:
    # Forgot Password Form
    st.markdown('''<div class="auth-card">
        <div class="auth-logo"><span class="icon">📈</span></div>
        <h1 class="auth-title">Reset Password</h1>
        <p class="auth-subtitle">Enter your email to receive a reset link</p>
    ''', unsafe_allow_html=True)

    with st.form("forgot_password_form", clear_on_submit=False):
        reset_email = st.text_input(
            "Email Address",
            placeholder="name@example.com",
            key="reset_email"
        )

        col1, col2 = st.columns(2)
        with col1:
            send_reset_button = st.form_submit_button("Send Link", type="primary", use_container_width=True)
        with col2:
            cancel_button = st.form_submit_button("Cancel", use_container_width=True)

    if cancel_button:
        st.session_state.show_forgot_password = False
        st.rerun()

    if send_reset_button:
        if not reset_email:
            st.error("Please enter your email address")
        else:
            try:
                with st.spinner("Sending reset link..."):
                    token = auth.request_password_reset(reset_email)
                    st.success("If an account exists, a reset link has been sent!")
                    st.info("Check your email inbox. The link expires in 1 hour.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    st.markdown('<div class="auth-divider">or</div>', unsafe_allow_html=True)

    if st.button("Back to Sign In", use_container_width=True):
        st.session_state.show_forgot_password = False
        st.rerun()

else:
    # Sign In Form
    st.markdown('''<div class="auth-card">
        <div class="auth-logo"><span class="icon">📈</span></div>
        <h1 class="auth-title">Welcome Back</h1>
        <p class="auth-subtitle">Sign in to access your dashboard</p>
    ''', unsafe_allow_html=True)

    with st.form("signin_form", clear_on_submit=False):
        email = st.text_input(
            "Email Address",
            placeholder="name@example.com",
            key="signin_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="signin_password"
        )

        submit_button = st.form_submit_button("Sign In", type="primary", use_container_width=True)

    # Forgot password link
    if st.button("Forgot Password?", key="forgot_password_btn", use_container_width=True):
        st.session_state.show_forgot_password = True
        st.rerun()

    # Handle sign in
    if submit_button:
        if not email or not password:
            st.error("Please enter both email and password")
        else:
            try:
                with st.spinner("Signing in..."):
                    user = auth.authenticate(email, password)

                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user['id']
                        st.session_state.user_email = user['email']
                        st.success("Welcome back!")
                        st.switch_page("app.py")
                    else:
                        st.error("Invalid email or password")
            except AuthError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Sign up link
    st.markdown('<div class="auth-divider">New here?</div>', unsafe_allow_html=True)

    if st.button("Create an Account", key="goto_signup", use_container_width=True):
        st.switch_page("pages/signup.py")

st.markdown('</div>', unsafe_allow_html=True)
