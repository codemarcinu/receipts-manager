from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.database.models import db
from src.web.views import bp, register_error_handlers
from src.database.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicjalizacja rozszerzeń
    db.init_app(app)
    migrate = Migrate(app, db)

    # Rejestracja blueprintów
    app.register_blueprint(bp)
    register_error_handlers(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)