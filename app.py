"""
app.py
Entry point for the Flask application.
"""

from src.api import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
