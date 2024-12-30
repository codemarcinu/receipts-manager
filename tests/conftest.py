import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.web import create_app
from src.database import db as _db
from datetime import datetime
from src.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    app = create_app(TestConfig)
    
    # Utworzenie kontekstu aplikacji
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope='function')
def db(app):
    """Create a new database for each test."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.close()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()