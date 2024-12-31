from flask import Flask
from flask_compress import Compress
from src.database import db, migrate
from src.config import Config
import logging


def create_app():
    app = Flask(__name__)
    Compress(app)
    
    # Enable Gzip compression for CSS files
    app.config['COMPRESS_MIMETYPES'] = ['text/css', 'text/html', 'application/javascript']
    app.config['COMPRESS_LEVEL'] = 6
    app.config['COMPRESS_MIN_SIZE'] = 500

    app.config.from_object(Config)

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
    from .views import bp as receipts_bp
    from .error_handlers import errors as errors_bp

    app.register_blueprint(receipts_bp)
    app.register_blueprint(errors_bp)

    return app