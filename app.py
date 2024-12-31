from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Create required directories
    Config.init_app(app)
    
    # Import and register blueprints
    from src.routes import main
    app.register_blueprint(main)
    
    # Import models for migrations
    from src.models import Receipt, ReceiptItem
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
