from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
import logging
import os

db = SQLAlchemy()
migrate = Migrate()

from .forms import ReceiptUploadForm, ReceiptVerificationForm
from .views import bp as receipts_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicjalizacja rozszerzeń
    db.init_app(app)
    migrate.init_app(app, db)

    # Konfiguracja logowania
    logging.basicConfig(
        filename=app.config.get('LOG_FILE', 'app.log'),
        level=app.config.get('LOG_LEVEL', logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Rejestracja blueprintów
    from src.views import bp as receipts_bp, register_error_handlers
    app.register_blueprint(receipts_bp)
    
    # Rejestracja error handlerów
    register_error_handlers(app)

    return app