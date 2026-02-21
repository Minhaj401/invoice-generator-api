"""
Flask Application Factory
"""

import logging
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    """
    Create and configure Flask application.
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask app instance
    """
    
    logger.info("Starting Flask application initialization...")
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    logger.info(f"Flask environment: {app.config.get('FLASK_ENV', 'production')}")
    logger.info(f"Debug mode: {app.config.get('FLASK_DEBUG', False)}")
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    logger.info("CORS enabled for /api/* endpoints")
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    logger.info("API blueprint registered")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404 Not Found: {error}")
        return jsonify({
            'error': 'Not found',
            'message': 'The requested endpoint does not exist'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        logger.warning(f"405 Method Not Allowed: {error}")
        return jsonify({
            'error': 'Method not allowed',
            'message': 'The method is not allowed for the requested URL'
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 Internal Server Error: {error}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    # Root endpoint - Serve the frontend
    @app.route('/')
    def index():
        from flask import send_from_directory
        import os
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return send_from_directory(root_dir, 'index.html')
    
    logger.info("Flask application initialization completed successfully!")
    return app
