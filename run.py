import os
import logging
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log startup information
logger.info("="*60)
logger.info("INVOICE GENERATOR API - STARTING UP")
logger.info("="*60)
logger.info(f"Python: {os.sys.version}")
logger.info(f"Working Directory: {os.getcwd()}")
logger.info(f"PORT: {os.getenv('PORT', '5000')}")

# Check critical environment variables
if not os.getenv('GEMINI_API_KEY'):
    logger.warning("⚠️  GEMINI_API_KEY not set! Invoice generation will fail.")
else:
    logger.info("✓ GEMINI_API_KEY is configured")

logger.info(f"Business Name: {os.getenv('BUSINESS_NAME', 'Your Business Name')}")
logger.info("="*60)

# Create Flask app
logger.info("Creating Flask application...")
app = create_app()
logger.info("Flask application created successfully!")

if __name__ == '__main__':
    logger.info("Starting development server on 0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
