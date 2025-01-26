from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    
    with app.app_context():
        # Import parts of our application
        from .routes import main_routes  # Example route import
        
        # Register Blueprints
        app.register_blueprint(main_routes)
        
        # Create tables for our models
        db.create_all()
    
    return app