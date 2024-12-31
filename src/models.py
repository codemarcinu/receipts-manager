from app import db
from datetime import datetime

class Receipt(db.Model):
    __tablename__ = 'receipts'

    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    products = db.relationship('ReceiptItem', backref='receipt', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'store': self.store,
            'date': self.date.isoformat(),
            'total': self.total
        }

class ReceiptItem(db.Model):
    __tablename__ = 'receipt_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipts.id'), nullable=False)