#!/usr/bin/env python
# coding: utf-8
"""
Sign Up page for user registration.
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import auth module
sys.path.insert(0, str(Path(__file__).parent.parent))

import auth
from auth import AuthError

st.set_page_config(
    page_title="Sign Up - Multi-Agent Stock Analyst",
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

    /* Feature list */
    .feature-list {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 4px;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
    }

    .feature-item {
        display: flex;
        align-items: center;
        color: #374151;
        font-size: 0.85rem;
        padding: 0.25rem 0;
    }

    .feature-item .check {
        color: #667eea;
        margin-right: 0.75rem;
        font-weight: bold;
    }

    /* Success/Error messages */
    .stAlert {
        border-radius: 4px;
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

# Check if user is already authenticated
if 'authenticated' in st.session_state and st.session_state.authenticated:
    st.switch_page("app.py")

# Main card container with all header content
st.markdown('''<div class="auth-card">
    <div class="auth-logo"><span class="icon">📈</span></div>
    <h1 class="auth-title">Create Account</h1>
    <p class="auth-subtitle">Get started with AI-powered stock analysis</p>
    <div class="feature-list">
        <div class="feature-item"><span class="check">✓</span> ML-powered price predictions</div>
        <div class="feature-item"><span class="check">✓</span> Technical & fundamental analysis</div>
        <div class="feature-item"><span class="check">✓</span> AI-generated insights</div>
    </div>
''', unsafe_allow_html=True)

# Sign up form
with st.form("signup_form", clear_on_submit=False):
    email = st.text_input(
        "Email Address",
        placeholder="name@example.com",
        help="We'll send a verification link to this email"
    )

    submit_button = st.form_submit_button("Create Account", type="primary", use_container_width=True)

if submit_button:
    if not email:
        st.error("Please enter your email address")
    else:
        try:
            with st.spinner("Creating your account..."):
                user_id, token = auth.register_user(email)
                st.success("Account created successfully!")
                st.info("""
                **Check your email!**
                We've sent a verification link to complete your registration.
                The link expires in 24 hours.
                """)
        except AuthError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Sign in link
st.markdown('<div class="auth-divider">Already have an account?</div>', unsafe_allow_html=True)

if st.button("Sign In", key="goto_signin", use_container_width=True):
    st.switch_page("pages/signin.py")

st.markdown('</div>', unsafe_allow_html=True)
