"""
Flask Application Factory
"""

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config


def create_app(config_class=Config):
    """
    Create and configure Flask application.
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask app instance
    """
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested endpoint does not exist'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Method not allowed',
            'message': 'The method is not allowed for the requested URL'
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
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
    
    return app
