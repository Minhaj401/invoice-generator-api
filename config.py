import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Google Gemini AI
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-2.0-flash-exp'  # Free tier model
    
    # Business Details
    BUSINESS_NAME = os.getenv('BUSINESS_NAME', 'Your Business Name')
    BUSINESS_ADDRESS = os.getenv('BUSINESS_ADDRESS', '123 Business Street, City, State - 123456')
    BUSINESS_PHONE = os.getenv('BUSINESS_PHONE', '+91-1234567890')
    BUSINESS_EMAIL = os.getenv('BUSINESS_EMAIL', 'info@yourbusiness.com')
    BUSINESS_GST = os.getenv('BUSINESS_GST', '22AAAAA0000A1Z5')
    
    # Tax Configuration
    GST_RATE = 0.18  # 18%
    
    # Invoice Settings
    INVOICE_PREFIX = 'INV'
    CURRENCY = 'INR'
    CURRENCY_SYMBOL = 'Rs.'
    
    # File Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    COUNTER_FILE = os.path.join(BASE_DIR, 'invoice_counter.txt')
