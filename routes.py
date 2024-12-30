from flask import Blueprint, render_template
from src.database.models import Receipt, Product, Category

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/receipts')
def receipts():
    return render_template('receipts.html')