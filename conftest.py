import os
import sys
import pytest
from src.web import create_app
from src.database.models import Base
from config import Config

# Add project root and src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src'))

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    with app.app_context():
        Base.metadata.create_all(app.db.engine)
        yield app.db
        Base.metadata.drop_all(app.db.engine)