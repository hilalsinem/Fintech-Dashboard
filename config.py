import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'fintech_dashboard'),
    'user': os.getenv('DB_USER', 'fintech_user'),
    'password': os.getenv('DB_PASSWORD', 'your_password')
}

# Dashboard configuration
DASHBOARD_CONFIG = {
    'title': 'Fintech Transaction Dashboard',
    'description': 'Real-time financial transaction monitoring and analysis',
    'theme': 'light'
}

# Analysis configuration
ANALYSIS_CONFIG = {
    'fraud_threshold': 3.0,  # Z-score threshold for fraud detection
    'min_transactions': 10,  # Minimum transactions for analysis
    'time_windows': ['daily', 'weekly', 'monthly']
}