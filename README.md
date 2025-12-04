# 🤖 Multi-Agent Stock Analyst

An AI-powered stock analysis system that combines Machine Learning, Technical Analysis, and Fundamental Analysis to provide comprehensive trading recommendations. Built with Google Gemini AI and a multi-agent architecture.

## ✨ Features

- **🤖 ML Agent**: Predicts stock prices using Random Forest Regressor with technical indicators
- **📉 Technical Agent**: Calculates RSI (Relative Strength Index) and identifies market trends
- **💼 Fundamental Agent**: Analyzes PE ratio, market cap, and analyst recommendations
- **🧠 AI Manager**: Google Gemini AI combines insights from all agents to generate trading recommendations
- **🖥️ Web UI**: Beautiful Streamlit interface for easy interaction
- **⌨️ CLI Mode**: Command-line interface for quick analysis

## 🏗️ Architecture

The system uses a multi-agent architecture where specialized agents work together:

1. **ML Agent** → Uses Random Forest to predict next-day stock prices
2. **Technical Agent** → Calculates technical indicators (RSI, trends)
3. **Fundamental Agent** → Fetches fundamental metrics (PE ratio, market cap)
4. **AI Manager** → Google Gemini AI synthesizes all data into actionable recommendations

## 📋 Prerequisites

- Python 3.8 or higher
- Google Generative AI API key ([Get one here](https://makersuite.google.com/app/apikey))

## 🚀 Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd MultiAgentStockAnalysis
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   
   Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
   
   Add your Google API key to the `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
   
   > ⚠️ **Important**: Never commit your `.env` file to version control. Add it to `.gitignore`.

## 🎯 Usage

### Web UI (Recommended)

Launch the Streamlit web interface:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

**Features:**
- Enter stock symbol in the sidebar
- Click "Analyze Stock" to get AI-powered recommendations
- View detailed data from all three agents in an expandable section
- Clean, intuitive interface

### Command Line Interface

Run the CLI version:

```bash
python multi-agent-stock-analyst.py
```

**Usage:**
- Enter a stock ticker symbol when prompted (e.g., `AAPL`, `MSFT`, `GOOGL`)
- Type `quit` to exit

**Example:**
```
🤖 AI Agent Online. Internet check: PASSED

Stock Ticker (or 'quit'): AAPL
🤖 Quant Agent: Fetching data for AAPL...
   >>> ML Success: Predicted UP 📈
[AI recommendation will be displayed here]
```

## 📁 Project Structure

```
MultiAgentStockAnalysis/
├── multi-agent-stock-analyst.py  # Main analysis engine with agent functions
├── app.py                        # Streamlit web UI
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (create this)
└── README.md                     # This file
```

## 📦 Dependencies

- `yfinance` - Yahoo Finance data fetching
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `google-generativeai` - Google Gemini AI integration
- `scikit-learn` - Machine learning models
- `python-dotenv` - Environment variable management
- `streamlit` - Web UI framework

## 🔧 Configuration

### Environment Variables

The application requires a `.env` file with the following variable:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### Getting a Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

## 📊 Example Analysis

When you analyze a stock (e.g., `AAPL`), the system:

1. **ML Agent** provides:
   - Current price
   - Predicted next-day price
   - Expected direction (UP/DOWN)
   - Expected percentage change

2. **Technical Agent** provides:
   - RSI (Relative Strength Index)
   - Market trend (Bullish/Bearish)

3. **Fundamental Agent** provides:
   - PE Ratio
   - Market Cap
   - Analyst Recommendation

4. **AI Manager** synthesizes all data into a comprehensive trading recommendation

## 🛠️ How It Works

1. **Data Collection**: Fetches historical stock data from Yahoo Finance
2. **Feature Engineering**: Creates technical indicators (SMA, RSI)
3. **ML Prediction**: Trains Random Forest model on historical data
4. **Multi-Agent Analysis**: Each agent performs specialized analysis
5. **AI Synthesis**: Gemini AI combines all insights into actionable recommendations

## ⚠️ Important Notes

- **Data Source**: Stock data is fetched from Yahoo Finance (free, but may have rate limits)
- **ML Model**: Uses Random Forest with 50 estimators (configurable in code)
- **API Costs**: Google Gemini API usage may incur costs depending on your plan
- **Not Financial Advice**: This tool is for educational purposes only. Always do your own research before making investment decisions.

## 🐛 Troubleshooting

### API Key Issues
- Ensure `.env` file exists in the project root
- Verify `GOOGLE_API_KEY` is set correctly
- Check that the API key is valid and has sufficient quota

### Import Errors
- Run `pip install -r requirements.txt` to install all dependencies
- Ensure you're using Python 3.8 or higher

### Data Fetching Issues
- Check your internet connection
- Verify the stock ticker symbol is correct
- Some stocks may not have sufficient historical data

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on the repository.

---

**Disclaimer**: This tool is for educational and research purposes only. Stock market investments carry risk, and past performance does not guarantee future results. Always consult with a qualified financial advisor before making investment decisions.

