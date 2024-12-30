from flask import (

    Blueprint,

    render_template,

    request,

    flash,

    redirect,

    url_for,

    current_app,

    jsonify
)

from src.database.models import Receipt, Product, Category

from src.database import db

from .forms import ReceiptUploadForm, ReceiptVerificationForm
import logging

from sqlalchemy import func
from datetime import datetime

from werkzeug.utils import secure_filename
import os


# Konfiguracja loggera

logger = logging.getLogger(__name__)


# Tworzenie blueprintów

bp = Blueprint('receipts', __name__, url_prefix='/receipts')

errors = Blueprint('errors', __name__)


# Obsługa błędów

@errors.app_errorhandler(404)

def not_found_error(error):

    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)

def internal_error(error):

    db.session.rollback()

    return render_template('errors/500.html'), 500


@errors.app_errorhandler(403)

def forbidden_error(error):

    return render_template('errors/403.html'), 403


# Widoki główne

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

    """Widok do uploadowania nowego paragonu."""

    form = ReceiptUploadForm()

    if form.validate_on_submit():

        try:

            # Zapisywanie pliku

            file = form.receipt_image.data

            filename = secure_filename(file.filename)

            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)


            # Tworzenie nowego paragonu
            db.session.add(Receipt(
                store_name=form.store_name.data,
                purchase_date=datetime.now().date(),

                total_amount=0,

                status='new'
            ))

            db.session.commit()


            flash('Paragon został pomyślnie dodany.', 'success')

            return redirect(url_for('receipts.verify_receipt', receipt_id=(Receipt(
                store_name=form.store_name.data,
                purchase_date=datetime.now().date(),
                total_amount=0,
                status='new'
            )).id))

        except Exception as e:

            logger.error(f"Błąd podczas uploadu paragonu: {str(e)}")

            flash('Wystąpił błąd podczas uploadu paragonu.', 'error')


    return render_template('upload.html', form=form)


@bp.route('/verify/<int:receipt_id>', methods=['GET', 'POST'])

def verify_receipt(receipt_id):

    """Widok do weryfikacji danych z paragonu."""

    receipt = Receipt.query.get_or_404(receipt_id)

    categories = Category.query.order_by(Category.name).all()


    if request.method == 'GET':

        form_data = {

            'receipt_id': receipt.id,

            'store_name': receipt.store_name,

            'purchase_date': receipt.purchase_date,

            'total_amount': receipt.total_amount,

            'products': [{

                'id': product.id,

                'name': product.name,

                'unit_price': product.unit_price,

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

                receipt.store_name = form.store_name.data

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

                            product.unit_price = product_form['unit_price'].data

                            product.quantity = product_form['quantity'].data

                            product.unit = product_form['unit'].data

                            product.category_id = product_form['category_id'].data or None

                            product.expiry_date = product_form['expiry_date'].data

                    else:

                        product = Product(

                            receipt_id=receipt.id,

                            name=product_form['name'].data,

                            unit_price=product_form['unit_price'].data,

                            quantity=product_form['quantity'].data,

                            unit=product_form['unit'].data,

                            category_id=product_form['category_id'].data or None,

                            expiry_date=product_form['expiry_date'].data
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