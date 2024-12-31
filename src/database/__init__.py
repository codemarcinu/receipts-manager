from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# Inicjalizacja obiektów SQLAlchemy i Migrate
db = SQLAlchemy()
migrate = Migrate()


def init_app(app):
    """Initialize database and migrations."""
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to ensure they are registered with SQLAlchemy
    from . import models  # noqa

    # Create tables if they don't exist (development only)
    if app.config['FLASK_ENV'] == 'development':
        with app.app_context():
            db.create_all()

    return db