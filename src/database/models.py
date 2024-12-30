# models.py
from datetime import datetime
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Date, DateTime
from sqlalchemy.orm import relationship

db = SQLAlchemy()
Base = declarative_base()

class BaseModel(db.Model):
    """Base model class for common columns and methods."""
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def save(self):
        """Save the model instance to database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Delete the model instance from database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class Receipt(BaseModel):
    __tablename__ = 'receipts'
    
    store = Column(String(128), nullable=False)
    date = Column(Date, nullable=False)
    total = Column(Float, nullable=False)
    image_filename = Column(String(256), nullable=True)
    products = relationship('ReceiptItem', back_populates='receipt', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Receipt {self.id} - {self.store} on {self.date}>"

class ReceiptItem(BaseModel):
    __tablename__ = 'receipt_items'
    
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit = Column(String(50), nullable=False)
    receipt_id = Column(Integer, ForeignKey('receipts.id', ondelete='CASCADE'), nullable=False)
    receipt = relationship('Receipt', back_populates='products')

    def __repr__(self):
        return f"<ReceiptItem {self.name} - {self.quantity} {self.unit}>"

class Category(BaseModel):
    __tablename__ = 'categories'
    
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    products = relationship('Product', back_populates='category', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Category {self.name}>"

class Product(BaseModel):
    __tablename__ = 'products'
    
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    category = relationship('Category', back_populates='products')

    def __repr__(self):
        return f"<Product {self.name}>"

class ProductStatus(BaseModel):
    __tablename__ = 'product_status'
    
    status = Column(String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<ProductStatus {self.status}>"

# config.py
class Config:
    DATABASE_URL = "sqlite:///development.db"

# routes.py
from flask import Blueprint, request, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "Welcome to Receipts Manager"})

@main.route('/upload', methods=['POST'])
def upload():
    if 'receipt' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    return jsonify({'success': True}), 200

@main.route('/save', methods=['POST'])
def save_receipt():
    data = request.get_json()
    if not data or 'store' not in data:
        return jsonify({'success': False, 'message': 'Invalid data'}), 400
    return jsonify({'success': True}), 200

@main.route('/receipts', methods=['GET'])
def list_receipts():
    return jsonify({'receipts': []}), 200

@main.route('/receipt/<int:receipt_id>', methods=['GET'])
def view_receipt(receipt_id):
    return jsonify({'receipt': {}}), 200

# services/ocr.py
class OCRService:
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path

    def process_image(self, image_path):
        pass

# database/manager.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

class DatabaseManager:
    def __init__(self, database_url: str = None):
        self.engine = create_engine(database_url or Config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()
    
    def dispose_engine(self):
        self.engine.dispose()

# app.py
from flask import Flask
from routes import main
from database.manager import DatabaseManager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Database
    db_manager = DatabaseManager()
    db_manager.engine.connect()
    from database.models import Base
    Base.metadata.create_all(db_manager.engine)
    
    # Register Blueprints
    app.register_blueprint(main)
    
    return app

# tests/conftest.py
import sys
import os
import pytest
from app import create_app
from database.manager import DatabaseManager
from config import Config

@pytest.fixture(scope='session')
def app():
    app = create_app(Config)
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_db():
    """Creates a temporary database for tests"""
    test_db_url = "sqlite:///test_receipts.db"
    manager = DatabaseManager(test_db_url)
    manager.engine.connect()
    from database.models import Base
    Base.metadata.create_all(manager.engine)

    yield test_db_url

    manager.dispose_engine()
    os.remove("test_receipts.db")

@pytest.fixture
def db_manager(test_db):
    """Creates an instance of DatabaseManager with the test database"""
    os.environ['DATABASE_URL'] = test_db
    manager = DatabaseManager()
    yield manager
    manager.dispose_engine()
# src/database/models.py
from src.database.manager import DatabaseManager
# src/database/models.py
from src.database.manager import DatabaseManager