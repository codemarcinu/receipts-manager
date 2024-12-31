from flask import Blueprint, request, jsonify, render_template
from src.models import Receipt, ReceiptItem, db
from werkzeug.exceptions import BadRequest
import datetime

main = Blueprint('main', __name__)  # Ensure no url_prefix

@main.route('/api/message')
def get_message():
    return jsonify({'message': 'Welcome to Receipts Manager'})

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    if 'receipt' not in request.files:
        raise BadRequest('No file part')
    
    file = request.files['receipt']
    if file.filename == '':
        raise BadRequest('No selected file')
    
    # TODO: Implement file saving and OCR processing
    return jsonify({'success': True, 'message': 'File received'}), 201

@main.route('/save', methods=['POST'])
def save_receipt():
    data = request.get_json()
    
    if not data or 'store' not in data:
        raise BadRequest('Invalid receipt data')
    
    try:
        receipt = Receipt(
            store=data['store'],
            date=datetime.datetime.strptime(data['date'], '%Y-%m-%d').date(),
            total=float(data['total'])
        )
        
        db.session.add(receipt)
        
        if 'items' in data:
            for item_data in data['items']:
                receipt_item = ReceiptItem(
                    name=item_data['name'],
                    price=float(item_data['price']),
                    quantity=int(item_data['quantity']),
                    unit=item_data['unit'],
                    receipt=receipt
                )
                db.session.add(receipt_item)
        
        db.session.commit()
        return jsonify({'success': True, 'receipt_id': receipt.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/receipts', methods=['GET'])
def list_receipts():
    receipts = Receipt.query.order_by(Receipt.date.desc()).all()
    return jsonify({
        'receipts': [
            {
                'id': r.id, 
                'store': r.store, 
                'date': r.date.isoformat(), 
                'total': r.total
            } for r in receipts
        ]
    }), 200

@main.route('/receipt/<int:receipt_id>', methods=['GET'])
def view_receipt(receipt_id):
    receipt = Receipt.query.get_or_404(receipt_id)
    return jsonify({
        'receipt': {
            'id': receipt.id,
            'store': receipt.store,
            'date': receipt.date.isoformat(),
            'total': receipt.total,
            'items': [
                {
                    'name': item.name,
                    'price': item.price,
                    'quantity': item.quantity,
                    'unit': item.unit
                } for item in receipt.products
            ]
        }
    }), 200

@main.route('/receipt/new')
def new_receipt():
    return render_template('receipt_form.html')

@main.route('/receipt/list')
def receipt_list_view():
    return render_template('receipt_list.html')