"""
Testy dla operacji CRUD na paragonach.
"""
from flask_sqlalchemy import SQLAlchemy
import pytest
from datetime import date
from typing import Any
from src.database.models import Receipt, Product
from src.database import db


@pytest.fixture
def test_receipt(db: SQLAlchemy):
    """Fixture tworzący testowy paragon z produktami."""
    receipt = Receipt(
        purchase_date=date.today(),
        store_name="Test Store",
        total_amount=100.00,
        status="new"
    )
    db.session.add(receipt)
    db.session.flush()  # Potrzebujemy ID paragonu przed dodaniem produktów

    # Dodanie testowych produktów
    products = [
        Product(
            receipt_id=receipt.id,
            name=f"Product {i}",
            unit_price=10.00,
            quantity=1,
            unit="szt"
        ) for i in range(3)
    ]
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    
    yield receipt
    
    # Czyszczenie po teście (jeśli paragon nadal istnieje)
    try:
        db_receipt = db.session.get(Receipt, receipt.id)
        if db_receipt:
            db.session.delete(db_receipt)
            db.session.commit()
    except:
        db.session.rollback()


def test_delete_receipt_success(client: Any, test_receipt: Receipt):
    """Test poprawnego usuwania paragonu."""
    # Przygotowanie
    receipt_id = test_receipt.id
    product_ids = [p.id for p in test_receipt.products]

    # Wykonanie
    response = client.delete(f'/receipts/{receipt_id}')
    
    # Sprawdzenie
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    
    # Sprawdzenie czy paragon został usunięty
    assert db.session.get(Receipt, receipt_id) is None
    
    # Sprawdzenie czy produkty zostały usunięte
    for product_id in product_ids:
        assert db.session.get(Product, product_id) is None


def test_delete_nonexistent_receipt(client: Any, db: Any):
    """Test próby usunięcia nieistniejącego paragonu."""
    # Upewnijmy się, że baza danych jest zainicjalizowana
    response = client.delete('/receipts/99999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False
    assert 'nie znaleziono' in data['message'].lower()


def test_delete_receipt_with_db_error(client: Any, test_receipt: Receipt, monkeypatch: Any):
    """Test obsługi błędu bazy danych podczas usuwania."""
    def mock_db_error(*args, **kwargs):
        raise Exception("Database error")
    
    # Podmiana metody delete na wersję wywołującą błąd
    monkeypatch.setattr(db.session, 'delete', mock_db_error)
    
    response = client.delete(f'/receipts/{test_receipt.id}')
    
    assert response.status_code == 500
    data = response.get_json()
    assert data['success'] is False
    assert 'błąd' in data['message'].lower()
    
    # Sprawdzenie czy paragon nadal istnieje (rollback zadziałał)
    assert db.session.get(Receipt, test_receipt.id) is not None