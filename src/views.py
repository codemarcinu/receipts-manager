from flask import (
    Blueprint, render_template, request, flash,
    redirect, url_for, current_app, jsonify
)
from .database.models import Receipt, Product, Category, db
from src.forms import ReceiptUploadForm, ReceiptVerificationForm
import logging
from sqlalchemy import func
from datetime import datetime
from werkzeug.utils import secure_filename
import os

# Logger configuration
logger = logging.getLogger(__name__)

# Blueprint definitions
bp = Blueprint('receipts', __name__, url_prefix='/receipts')
errors = Blueprint('errors', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Error handlers
@errors.app_errorhandler(404)
def not_found_error(error):
    current_app.logger.error(f'Page not found: {request.url}')
    current_app.logger.info(f'Template folders: {current_app.jinja_loader.searchpath}')
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error(f'Server Error: {error}')
    db.session.rollback()
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(403)
def forbidden_error(error):
    current_app.logger.error(f'Forbidden access: {request.url}')
    return render_template('errors/403.html'), 403

def register_error_handlers(app):
    """Register error handlers and ensure template directory is properly configured"""
    # Dodaj debugowanie ścieżki do templatek
    app.logger.info(f'Current working directory: {os.getcwd()}')
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    app.logger.info(f'Template directory: {template_dir}')
    
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
        app.logger.info(f'Created template directory at: {template_dir}')
    
    errors_dir = os.path.join(template_dir, 'errors')
    if not os.path.exists(errors_dir):
        os.makedirs(errors_dir)
        app.logger.info(f'Created errors directory at: {errors_dir}')
    
    app.register_blueprint(errors)
    app.logger.info('Error handlers registered')
    return app

def verify_required_templates():
    """Sprawdź czy wszystkie wymagane pliki template istnieją"""
    required_templates = [
        'index.html',
        'receipt_list.html',
        'upload.html',
        'verify.html',
        'errors/404.html',
        'errors/500.html',
        'errors/403.html'
    ]
    
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    missing_templates = []
    
    for template in required_templates:
        template_path = os.path.join(template_dir, template)
        if not os.path.exists(template_path):
            missing_templates.append(template)
    
    return missing_templates

def init_app(app):
    """Inicjalizacja aplikacji z dodatkowymi sprawdzeniami"""
    register_error_handlers(app)
    
    # Sprawdź szablony przy starcie
    missing_templates = verify_required_templates()
    if missing_templates:
        app.logger.error(f"Brakujące szablony: {', '.join(missing_templates)}")
        raise RuntimeError(f"Brakujące wymagane szablony: {', '.join(missing_templates)}")
    
    # Upewnij się, że folder na uploady istnieje
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        app.logger.info(f"Utworzono folder na uploady: {app.config['UPLOAD_FOLDER']}")

    return app

# Main views

@bp.route('/')
def index():
    """Strona główna aplikacji."""
    return render_template('index.html')

@bp.route('/list')
def receipt_list():
    """Lista wszystkich paragonów."""
    receipts = Receipt.query.order_by(Receipt.purchase_date.desc()).all()
    return render_template('receipt_list.html', receipts=receipts)

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """View for uploading a new receipt."""
    form = ReceiptUploadForm()
    
    if form.validate_on_submit():
        try:
            file = form.receipt_image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                receipt = Receipt(
                    store=form.store.data,
                    purchase_date=form.purchase_date.data,
                    total_amount=form.total_amount.data,
                    image_filename=filename,
                    created_at=datetime.utcnow()  # Dodane pole created_at
                )
                db.session.add(receipt)
                db.session.commit()

                flash('Paragon został pomyślnie dodany.', 'success')
                return redirect(url_for('receipts.index'))
            else:
                flash('Nieprawidłowy format pliku lub brak pliku.', 'danger')
        except Exception as e:
            db.session.rollback()
            logger.error(f"Błąd podczas dodawania paragonu: {str(e)}")
            flash(f'Wystąpił błąd podczas dodawania paragonu: {str(e)}', 'danger')

    return render_template('upload.html', form=form)

@bp.route('/verify/<int:receipt_id>', methods=['GET', 'POST'])
def verify_receipt(receipt_id):
    """Widok do weryfikacji danych z paragonu."""
    receipt = Receipt.query.get_or_404(receipt_id)
    categories = Category.query.order_by(Category.name).all()

    if request.method == 'GET':
        form_data = {
            'receipt_id': receipt.id,
            'store': receipt.store,
            'purchase_date': receipt.purchase_date,
            'total_amount': receipt.total_amount,
            'products': [{
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': product.quantity,
                'unit': product.unit,
                'category_id': product.category_id or 0,
                'expiry_date': product.expiry_date
            } for product in receipt.products]
        }
        form = ReceiptVerificationForm(data=form_data, categories=categories)
    else:
        form = ReceiptVerificationForm(categories=categories)
        if form.validate_on_submit():
            try:
                receipt.store = form.store.data
                receipt.purchase_date = form.purchase_date.data
                receipt.total_amount = form.total_amount.data
                receipt.status = 'verified'

                existing_product_ids = {p.id for p in receipt.products}
                form_product_ids = {
                    int(p['id'].data) for p in form.products
                    if p['id'].data
                }

                # Usuwanie produktów, których nie ma w formularzu
                for product in receipt.products:
                    if product.id not in form_product_ids:
                        db.session.delete(product)

                # Aktualizacja/dodawanie produktów
                for product_form in form.products:
                    product_id = product_form['id'].data
                    if product_id:
                        product = Product.query.get(product_id)
                        if product:
                            product.name = product_form['name'].data
                            product.price = product_form['price'].data
                            product.quantity = product_form['quantity'].data
                            product.unit = product_form['unit'].data
                            product.category_id = product_form['category_id'].data or None
                            product.expiry_date = product_form['expiry_date'].data
                    else:
                        product = Product(
                            name=product_form['name'].data,
                            price=product_form['price'].data,
                            quantity=product_form['quantity'].data,
                            unit=product_form['unit'].data,
                            category_id=product_form['category_id'].data or None,
                            expiry_date=product_form['expiry_date'].data,
                            receipt=receipt
                        )
                        db.session.add(product)

                db.session.commit()
                flash('Paragon został pomyślnie zweryfikowany.', 'success')
                return redirect(url_for('receipts.receipt_list'))

            except Exception as e:
                logger.error(f"Błąd podczas zapisywania danych: {str(e)}")
                db.session.rollback()
                flash('Wystąpił błąd podczas zapisywania danych.', 'error')

    return render_template('verify.html', form=form, receipt=receipt)

@bp.route('/api/products/suggestions', methods=['GET'])
def get_product_suggestions():
    """Endpoint API zwracający sugestie nazw produktów."""
    query = request.args.get('query', '').lower()
    if len(query) < 2:
        return jsonify([])

    # Pobierz unikalne nazwy produktów pasujące do zapytania
    suggestions = Product.query\
        .with_entities(Product.name, Product.unit, Product.category_id)\
        .filter(func.lower(Product.name).contains(query))\
        .group_by(Product.name, Product.unit, Product.category_id)\
        .order_by(func.count(Product.id).desc())\
        .limit(10)\
        .all()

    # Przygotuj dane do odpowiedzi
    results = [{
        'name': suggestion.name,
        'unit': suggestion.unit,
        'category_id': suggestion.category_id
    } for suggestion in suggestions]

    return jsonify(results)

@bp.route('/<int:receipt_id>', methods=['DELETE'])
def delete_receipt(receipt_id):
    """Endpoint do usuwania paragonu."""
    try:
        receipt = Receipt.query.get_or_404(receipt_id)
        
        # Zabezpieczenie przed przypadkowym usunięciem zweryfikowanego paragonu
        if receipt.status == 'verified':
            return jsonify({
                'success': False,
                'message': 'Nie można usunąć zweryfikowanego paragonu.'
            }), 403
            
        # Usuwanie powiązanego pliku
        if receipt.image_filename:
            try:
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], receipt.image_filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                logger.warning(f"Nie udało się usunąć pliku paragonu: {str(e)}")

        # Usuwanie paragonu z bazy
        db.session.delete(receipt)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Paragon został pomyślnie usunięty.'
        })

    except Exception as e:
        logger.error(f"Błąd podczas usuwania paragonu: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Wystąpił błąd podczas usuwania paragonu.'
        }), 500

def test_save_receipt(db_manager):
    """Test function for saving receipts - should be moved to tests directory"""
    receipt_data = {
        'store': 'Test Store',
        'purchase_date': '2024-01-20',
        'total_amount': 100.50,
        'products': [
            {
                'name': 'Test Product 1',
                'price': 25.25,
                'quantity': 2,
                'unit': 'szt'
            },
            {
                'name': 'Test Product 2',
                'price': 50.00,
                'quantity': 1,
                'unit': 'szt'
            }
        ]
    }

    # Zapisanie paragonu
    receipt = db_manager.save_receipt(receipt_data)

    # Sprawdzenie czy paragon został zapisany
    assert receipt.id is not None
    assert receipt.store == 'Test Store'
    assert receipt.total_amount == 100.50
    assert len(receipt.products.all()) == 2