# Multi-Agent Stock Analyst

An AI-powered stock analysis system that combines Machine Learning, Technical Analysis, and Fundamental Analysis to provide comprehensive trading recommendations. Built with Google Gemini AI and a multi-agent architecture.

## Features

- **ML Agent**: Predicts stock prices using Random Forest Regressor with technical indicators
- **Technical Agent**: Calculates RSI (Relative Strength Index) and identifies market trends
- **Fundamental Agent**: Analyzes PE ratio, market cap, and analyst recommendations
- **AI Manager**: Google Gemini AI combines insights from all agents to generate trading recommendations
- **User Authentication**: Email-based registration with verification and password reset
- **Web UI**: Clean Streamlit interface for easy interaction

## Architecture

The system uses a multi-agent architecture where specialized agents work together:

1. **ML Agent** - Uses Random Forest to predict next-day stock prices
2. **Technical Agent** - Calculates technical indicators (RSI, trends)
3. **Fundamental Agent** - Fetches fundamental metrics (PE ratio, market cap)
4. **AI Manager** - Google Gemini AI synthesizes all data into actionable recommendations

## Prerequisites

- Python 3.8 or higher
- Google Generative AI API key ([Get one here](https://makersuite.google.com/app/apikey))
- SMTP credentials for email functionality (Gmail recommended)

## Installation

### 1. Clone and Install Dependencies

```bash
cd MultiAgentStockAnalysis
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# SMTP Configuration (for authentication emails)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# Application URL (for email verification links)
APP_BASE_URL=http://localhost:8501
```

**Note**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`.

## Authentication Flow

1. **Sign Up**: User enters email address
2. **Email Verification**: Verification link sent to user's email
3. **Set Password**: User creates password after clicking verification link
4. **Sign In**: User logs in with email and password
5. **Forgot Password**: Reset link sent via email

Admin notifications are sent to the configured admin email on new registrations.

## Project Structure

```
MultiAgentStockAnalysis/
├── app.py                        # Main Streamlit application
├── multi-agent-stock-analyst.py  # Stock analysis engine
├── auth.py                       # Authentication module
├── config.py                     # Configuration settings
├── email_templates.py            # HTML email templates
├── pages/
│   ├── signin.py                 # Sign in page
│   ├── signup.py                 # Sign up page
│   ├── verify_email.py           # Email verification page
│   └── reset_password.py         # Password reset page
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── .dockerignore                 # Docker ignore file
├── .gitignore                    # Git ignore file
├── cloudbuild.yaml               # GCP Cloud Build config
├── DEPLOYMENT.md                 # Deployment guide
└── README.md                     # This file
```

## Docker Deployment

```bash
# Build the image
docker build -t multi-agent-stock-analyst .

# Run the container
docker run -p 8501:8501 \
  -e SMTP_USERNAME=your-email@gmail.com \
  -e SMTP_PASSWORD=your-app-password \
  -e APP_BASE_URL=http://localhost:8501 \
  multi-agent-stock-analyst
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed GCP deployment instructions.

## Dependencies

- `yfinance` - Yahoo Finance data fetching
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `google-generativeai` - Google Gemini AI integration
- `scikit-learn` - Machine learning models
- `streamlit` - Web UI framework
- `bcrypt` - Password hashing
- `email-validator` - Email validation
- `python-dotenv` - Environment variable management

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USERNAME` | SMTP username/email | - |
| `SMTP_PASSWORD` | SMTP password/app password | - |
| `FROM_EMAIL` | Sender email address | Same as SMTP_USERNAME |
| `APP_BASE_URL` | Application base URL | `http://localhost:8501` |
| `ADMIN_EMAIL` | Admin notification email | `dinesh.katiyar@trustassist.ai` |

### Token Expiration

- Email verification tokens: 24 hours
- Password reset tokens: 1 hour

## Security Features

- Bcrypt password hashing (12 rounds)
- Secure token generation using Python secrets
- Time-limited, single-use tokens
- Email validation before registration
- Minimum password length enforcement (8 characters)

## Troubleshooting

### Email Not Sending
- Verify SMTP credentials in `.env` file
- For Gmail, ensure you're using an App Password
- Check that "Less secure app access" is not required (use App Password instead)

### Database Issues
- Delete `auth.db` to reset the database
- Database is auto-created on first run

### Import Errors
- Run `pip install -r requirements.txt`
- Ensure Python 3.8 or higher

## Disclaimer

This tool is for educational and research purposes only. Stock market investments carry risk, and past performance does not guarantee future results. Always consult with a qualified financial advisor before making investment decisions.
