from flask import Flask
from src.database import db, migrate
from src.config import Config
import logging


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
    from src.views import bp as receipts_bp
    from src.error_handlers import errors as errors_bp

    app.register_blueprint(receipts_bp)
    app.register_blueprint(errors_bp)

    return app