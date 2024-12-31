import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.database.models import db
from src.web.views import bp, register_error_handlers
from src.database.config import Config

# Ładowanie zmiennych środowiskowych
load_dotenv()

# Inicjalizacja rozszerzeń
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Konfiguracja ścieżek
    app.config['UPLOAD_FOLDER'] = Path(app.root_path) / 'static' / 'uploads'
    app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)

    # Inicjalizacja rozszerzeń
    db.init_app(app)
    migrate = Migrate(app, db)

    # Initialize Database
    db_manager = DatabaseManager()
    db_manager.engine.connect()
    
    # Używamy relatywnej ścieżki importu
    from .database.models import Base
    Base.metadata.create_all(db_manager.engine)

    # Rejestracja blueprintów
    app.register_blueprint(bp)
    register_error_handlers(app)

    return app

if __name__ == "__main__":
    app = create_app()