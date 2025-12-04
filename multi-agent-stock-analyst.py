#!/usr/bin/env python
# coding: utf-8
"""
Multi-Agent Stock Analyst

A comprehensive stock analysis system that combines:
- Machine Learning predictions using Random Forest
- Technical analysis (RSI, trends)
- Fundamental analysis (PE ratio, market cap)
- AI-powered recommendations via Google Gemini

The system uses a multi-agent architecture where specialized agents work together
to provide comprehensive trading recommendations.

Usage:
    CLI Mode: python multi-agent-stock-analyst.py
    UI Mode: streamlit run app.py

Requirements:
    - GOOGLE_API_KEY in .env file
    - Internet connection for data fetching
"""

import os
import sys
import subprocess

# Auto-install yfinance if missing
try:
    import yfinance
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])
    import yfinance as yf
else:
    import yfinance as yf

import pandas as pd
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI with API key from environment
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)
    print("✅ API Key loaded successfully from .env file")
except Exception as e:
    print(f"⚠️ WARNING: API Key missing. Please add 'GOOGLE_API_KEY' to your .env file.")
    print(f"   Error: {str(e)}")


# ============================================================================
# AGENT FUNCTIONS
# ============================================================================

def get_ml_prediction(ticker: str) -> dict:
    """
    ML Agent: Predicts next-day stock price using Random Forest Regressor.
    
    This agent fetches historical stock data, engineers features (SMA indicators),
    trains a Random Forest model, and predicts the next trading day's closing price.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        dict: Dictionary containing:
            - current_price (float): Current closing price
            - ml_predicted_price (float): Predicted next-day price
            - predicted_direction (str): "UP 📈" or "DOWN 📉"
            - expected_change_pct (float): Expected percentage change
            - model_used (str): Name of the ML model
            OR
            - error (str): Error message if prediction fails
    
    Raises:
        Exception: Handled internally, returns error dict instead
    """
    try:
        print(f"🤖 Quant Agent: Fetching data for {ticker}...")
        
        # Fetch Data (Increased period to ensure enough data for rolling averages)
        stock = yf.Ticker(ticker)
        df = stock.history(period="1y") 
        
        # CHECK 1: Did we get data?
        if df.empty:
            return {"error": "Symbol not found or no data returned from Yahoo Finance."}

        # Feature Engineering
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['Target'] = df['Close'].shift(-1) # Target is tomorrow's price
        
        # CHECK 2: Remove NaNs created by rolling windows
        df = df.dropna()
        
        # CHECK 3: Do we still have enough data to train?
        if len(df) < 50:
            return {"error": "Not enough historical data to train ML model (Stock might be too new)."}

        # Define Features (X) and Target (y)
        feature_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_10', 'SMA_50']
        X = df[feature_cols]
        y = df['Target']

        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        # Model Training
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X_train, y_train)
        
        # Prediction for Tomorrow
        # We take the VERY LAST row of data to predict the NEXT unknown Close
        latest_data = df.iloc[[-1]][feature_cols]
        predicted_price = model.predict(latest_data)[0]
        current_close = df.iloc[-1]['Close']
        
        direction = "UP 📈" if predicted_price > current_close else "DOWN 📉"
        pct_change = ((predicted_price - current_close) / current_close) * 100

        print(f"   >>> ML Success: Predicted {direction}")

        return {
            "current_price": round(current_close, 2),
            "ml_predicted_price": round(predicted_price, 2),
            "predicted_direction": direction,
            "expected_change_pct": round(pct_change, 2),
            "model_used": "RandomForestRegressor"
        }

    except Exception as e:
        print(f"❌ ML CRASH DETECTED: {str(e)}")
        return {"error": f"ML Analysis failed internally: {str(e)}"}


def get_technical_analysis(ticker: str) -> dict:
    """
    Technical Agent: Performs technical analysis on stock data.
    
    Calculates Relative Strength Index (RSI) and determines market trend
    based on price movements over the last 6 months.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        dict: Dictionary containing:
            - RSI (float): Relative Strength Index (0-100)
            - Trend (str): "Bullish" or "Bearish"
            OR
            - error (str): Error message if analysis fails
    
    Raises:
        Exception: Handled internally, returns error dict instead
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="6mo")
        if df.empty: return {"error": "No data"}

        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return {
            "RSI": round(rsi.iloc[-1], 2),
            "Trend": "Bullish" if df['Close'].iloc[-1] > df['Close'].mean() else "Bearish"
        }
    except Exception as e:
        return {"error": str(e)}


def get_fundamental_health(ticker: str) -> dict:
    """
    Fundamental Agent: Analyzes fundamental financial metrics.
    
    Fetches fundamental data including PE ratio, market capitalization,
    and analyst recommendations from Yahoo Finance.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        dict: Dictionary containing:
            - PE_Ratio (float or str): Price-to-Earnings ratio or 'N/A'
            - Market_Cap (int or str): Market capitalization or 'N/A'
            - Analyst_Rec (str): Analyst recommendation (uppercase)
            OR
            - error (str): Error message if analysis fails
    
    Raises:
        Exception: Handled internally, returns error dict instead
    """
    try:
        info = yf.Ticker(ticker).info
        return {
            "PE_Ratio": info.get('trailingPE', 'N/A'),
            "Market_Cap": info.get('marketCap', 'N/A'),
            "Analyst_Rec": info.get('recommendationKey', 'none').upper()
        }
    except Exception:
        return {"error": "Could not fetch fundamentals"}


# ============================================================================
# AI AGENT INITIALIZATION
# ============================================================================

def initialize_agent():
    """
    Initialize the Google Gemini AI agent with multi-agent tools.
    
    Creates a GenerativeModel configured with:
    - Model: gemini-2.0-flash
    - Tools: ML prediction, technical analysis, fundamental analysis
    - System instruction: Hedge Fund Manager persona
    
    Returns:
        Chat: Initialized chat instance with automatic function calling enabled
    
    Note:
        Requires GOOGLE_API_KEY to be set in environment variables.
        The agent is configured to always run ML prediction first, then
        combine all agent insights into trading recommendations.
    """
    tools = [get_ml_prediction, get_technical_analysis, get_fundamental_health]
    
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash', 
        tools=tools,
        system_instruction="""
        You are a Hedge Fund Manager.
        1. ALWAYS run `get_ml_prediction` first.
        2. If the ML tool returns an "error" field, tell the user "I couldn't run the ML model because [reason]".
        3. Otherwise, combine ML, Technicals, and Fundamentals into a trading recommendation.
        """
    )
    
    return model.start_chat(enable_automatic_function_calling=True)


def analyze_stock(ticker: str, chat_instance=None) -> str:
    """
    Analyze a stock using all agents and return AI-generated recommendation.
    
    This function orchestrates the multi-agent analysis by sending a request
    to the Gemini AI agent, which automatically calls the ML, Technical, and
    Fundamental agents, then synthesizes their outputs into a recommendation.
    
    Args:
        ticker (str): Stock ticker symbol to analyze (e.g., 'AAPL', 'MSFT')
        chat_instance (Chat, optional): Pre-initialized chat instance.
            If None, a new agent will be initialized. Defaults to None.
    
    Returns:
        str: AI-generated analysis and trading recommendation text.
            Returns error message string if analysis fails.
    
    Example:
        >>> chat = initialize_agent()
        >>> recommendation = analyze_stock("AAPL", chat)
        >>> print(recommendation)
    """
    if chat_instance is None:
        chat_instance = initialize_agent()
    
    try:
        response = chat_instance.send_message(f"Analyze {ticker}")
        return response.text
    except Exception as e:
        return f"Agent Error: {str(e)}"


# ============================================================================
# Streamlit UI Mode
# ============================================================================

if __name__ == "__main__":
    """
    Main entry point for CLI mode.
    
    Runs an interactive command-line interface where users can enter
    stock tickers to get AI-powered analysis and recommendations.
    
    Usage:
        python multi-agent-stock-analyst.py
    
    Commands:
        - Enter stock ticker: Analyzes the stock and displays recommendation
        - 'quit': Exits the application
    """
    print("\n🤖 AI Agent Online. Internet check: " + ("PASSED" if "yfinance" in sys.modules else "FAILED"))
    chat = initialize_agent()
    
    while True:
        user_input = input("\nStock Ticker (or 'quit'): ")
        if user_input.lower() == "quit":
            break
        
        try:
            response = analyze_stock(user_input, chat)
            print(response)
        except Exception as e:
            print(f"Agent Error: {e}")

