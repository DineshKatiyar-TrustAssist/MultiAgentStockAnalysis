#!/usr/bin/env python
# coding: utf-8
"""
Streamlit Web UI for Multi-Agent Stock Analyst

This module provides a web-based user interface for the Multi-Agent Stock Analyst.
It imports the analysis functions from the main module and provides an interactive
Streamlit interface for stock analysis.

Usage:
    streamlit run app.py

Features:
    - Interactive stock symbol input
    - Real-time AI-powered analysis
    - Detailed agent data visualization
    - Clean, responsive UI design

Requirements:
    - Streamlit must be installed (pip install streamlit)
    - GOOGLE_API_KEY must be set in .env file
    - All dependencies from requirements.txt
"""

import streamlit as st
import importlib.util
import sys
from pathlib import Path

# Import the main module (handles filename with hyphens)
# This approach is necessary because Python module names cannot contain hyphens
module_path = Path(__file__).parent / "multi-agent-stock-analyst.py"
spec = importlib.util.spec_from_file_location("stock_analyst", module_path)
stock_analyst = importlib.util.module_from_spec(spec)
sys.modules["stock_analyst"] = stock_analyst
spec.loader.exec_module(stock_analyst)

from stock_analyst import (
    initialize_agent,
    analyze_stock,
    get_ml_prediction,
    get_technical_analysis,
    get_fundamental_health
)

# Configure Streamlit page
st.set_page_config(
    page_title="Multi-Agent Stock Analyst",
    page_icon="📈",
    layout="wide"
)

# Page header
st.title("🤖 Multi-Agent Stock Analyst")
st.markdown("**AI-Powered Stock Analysis using ML, Technical, and Fundamental Analysis**")

# Initialize AI agent in session state (persists across reruns)
if 'chat' not in st.session_state:
    with st.spinner("Initializing AI Agent..."):
        st.session_state.chat = initialize_agent()
    st.success("✅ AI Agent Online")

# Sidebar for input
with st.sidebar:
    st.header("📊 Stock Analysis")
    ticker_input = st.text_input(
        "Enter Stock Symbol",
        placeholder="e.g., AAPL, MSFT, GOOGL",
        help="Enter a valid stock ticker symbol"
    )
    analyze_button = st.button("Analyze Stock", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### How it works:")
    st.markdown("""
    1. **ML Agent**: Predicts price using Random Forest
    2. **Technical Agent**: Calculates RSI and trend
    3. **Fundamental Agent**: Analyzes PE ratio and market cap
    4. **AI Manager**: Combines all insights for recommendation
    """)

# Main content area - handle stock analysis
if analyze_button and ticker_input:
    ticker = ticker_input.upper().strip()
    
    if not ticker:
        st.warning("⚠️ Please enter a stock symbol")
    else:
        # Perform analysis with loading indicator
        with st.spinner(f"🔍 Analyzing {ticker}... This may take a moment."):
            try:
                # Get AI-generated recommendation
                recommendation = analyze_stock(ticker, st.session_state.chat)
                
                # Display main recommendation
                st.markdown("---")
                st.subheader(f"📊 Analysis for {ticker}")
                st.markdown(recommendation)
                
                # Display detailed agent data in expandable section
                with st.expander("📈 View Detailed Agent Data"):
                    col1, col2, col3 = st.columns(3)
                    
                    # ML Agent data
                    with col1:
                        st.markdown("### 🤖 ML Agent")
                        ml_data = get_ml_prediction(ticker)
                        if "error" in ml_data:
                            st.error(ml_data["error"])
                        else:
                            st.json(ml_data)
                    
                    # Technical Agent data
                    with col2:
                        st.markdown("### 📉 Technical Agent")
                        tech_data = get_technical_analysis(ticker)
                        if "error" in tech_data:
                            st.error(tech_data["error"])
                        else:
                            st.json(tech_data)
                    
                    # Fundamental Agent data
                    with col3:
                        st.markdown("### 💼 Fundamental Agent")
                        fund_data = get_fundamental_health(ticker)
                        if "error" in fund_data:
                            st.error(fund_data["error"])
                        else:
                            st.json(fund_data)
            
            except Exception as e:
                st.error(f"❌ Error analyzing {ticker}: {str(e)}")

elif analyze_button:
    st.warning("⚠️ Please enter a stock symbol before clicking Analyze")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Powered by Google Gemini AI • Data from Yahoo Finance"
    "</div>",
    unsafe_allow_html=True
)

