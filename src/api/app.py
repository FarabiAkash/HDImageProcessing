from flask import Flask
from .routes import upload, metadata, slice, analyze, statistics
from ..db.database import init_db

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(upload.bp)
    app.register_blueprint(metadata.bp)
    app.register_blueprint(slice.bp)
    app.register_blueprint(analyze.bp)
    app.register_blueprint(statistics.bp)
    
    # Initialize database
    init_db(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
