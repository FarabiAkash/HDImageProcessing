"""
__init__.py
Entry point for the Flask application. 
Defines the create_app() function which initializes Flask and registers blueprints.
"""

from flask import Flask
from src.api.routes import api_bp

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Register the blueprint for our API
    app.register_blueprint(api_bp, url_prefix='/')

    return app
