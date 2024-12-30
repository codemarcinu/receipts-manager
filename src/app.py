from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import main
from database.manager import DatabaseManager
from database.models import db, Base

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = config_class.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize Database
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Register Blueprints
    app.register_blueprint(main)
    
    return app