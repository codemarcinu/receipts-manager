from datetime import datetime
from sqlalchemy.sql import func
from src.database import db


class BaseModel(db.Model):
    """Base model class for common columns and methods."""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

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


class Category(BaseModel):
    """Model representing product categories."""
    __tablename__ = 'categories'

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    products = db.relationship('Product', back_populates='category', lazy='dynamic')

    def __repr__(self):
        return f"<Category {self.name}>"


class Receipt(BaseModel):
    """Model representing shopping receipts."""
    __tablename__ = 'receipts'

    purchase_date = db.Column(db.Date, nullable=False)
    store_name = db.Column(db.String(200), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='new')  # new, processing, verified
    ocr_text = db.Column(db.Text, nullable=True)  # Raw OCR text

    # Relationships
    products = db.relationship(
        'Product',
        back_populates='receipt',
        lazy='dynamic',
        cascade='all, delete-orphan'  # Dodane kaskadowe usuwanie
    )

    def __repr__(self):
        return f"<Receipt {self.store_name} {self.purchase_date}>"


class Product(BaseModel):
    """Model representing products from receipts."""
    __tablename__ = 'products'

    name = db.Column(db.String(200), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Numeric(10, 3), nullable=False)  # Allow for fractional quantities
    unit = db.Column(db.String(20), nullable=True)  # kg, szt, l, etc.
    expiry_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')  # active, consumed

    # Foreign keys
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipts.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # Relationships
    receipt = db.relationship('Receipt', back_populates='products')
    category = db.relationship('Category', back_populates='products')

    def __repr__(self):
        return f"<Product {self.name} {self.quantity}{self.unit}>"