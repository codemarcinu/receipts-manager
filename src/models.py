from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_connection_string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended to suppress warnings
db = SQLAlchemy(app)

class Receipt(db.Model):
    __tablename__ = 'receipts'

    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Dodaj inne kolumny w razie potrzeby
    # total_amount = db.Column(db.Float, nullable=False)
    # merchant = db.Column(db.String(100))

with app.app_context():
    db.create_all()  # Create tables

@app.route('/list')
def receipt_list():
    """List all receipts."""
    receipts = Receipt.query.order_by(Receipt.purchase_date.desc()).all()
    return render_template('receipt_list.html', receipts=receipts)

if __name__ == "__main__":
    app.run(debug=True)