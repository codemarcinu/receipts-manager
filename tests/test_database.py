import pytest
from src.database.manager import DatabaseManager
from src.database.models import Receipt, ReceiptItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime


@pytest.fixture
def test_db():
    """Tworzy tymczasową bazę danych dla testów"""
    test_db_path = "sqlite:///test_receipts.db"
    engine = create_engine(test_db_path)

    # Tworzenie tabel
    from src.database.models import Base
    Base.metadata.create_all(engine)

    yield test_db_path

    # Czyszczenie po testach
    os.remove("test_receipts.db")


@pytest.fixture
def db_manager(test_db):
    """Tworzy instancję DatabaseManager z testową bazą"""
    os.environ['DATABASE_URL'] = test_db
    manager = DatabaseManager()
    yield manager
    manager.session.close()


def test_save_receipt(db_manager):
    """Test zapisywania paragonu"""
    receipt_data = {
        'store': 'Test Store',
        'date': '2024-01-20',
        'total': 100.50,
        'items': [
            {
                'name': 'Test Product 1',
                'quantity': 2,
                'price': 25.25,
                'unit': 'szt'
            },
            {
                'name': 'Test Product 2',
                'quantity': 1,
                'price': 50.00,
                'unit': 'szt'
            }
        ]
    }

    # Zapisanie paragonu
    receipt = db_manager.save_receipt(receipt_data)

    # Sprawdzenie czy paragon został zapisany
    assert receipt.id is not None
    assert receipt.store == 'Test Store'
    assert receipt.total == 100.50
    assert len(receipt.items) == 2


def test_get_receipts(db_manager):
    """Test pobierania listy paragonów"""
    # Dodanie testowych paragonów
    for i in range(3):
        receipt_data = {
            'store': f'Test Store {i}',
            'date': '2024-01-20',
            'total': 100.00 + i,
            'items': [
                {
                    'name': f'Test Product {i}',
                    'quantity': 1,
                    'price': 100.00 + i,
                    'unit': 'szt'
                }
            ]
        }
        db_manager.save_receipt(receipt_data)

    # Pobranie paragonów
    receipts = db_manager.get_receipts()

    # Sprawdzenie wyników
    assert len(receipts) == 3
    assert all(isinstance(r, Receipt) for r in receipts)
    assert receipts[0].total > receipts[1].total  # Sprawdzenie sortowania


def test_get_receipt(db_manager):
    """Test pobierania pojedynczego paragonu"""
    # Dodanie testowego paragonu
    receipt_data = {
        'store': 'Test Store',
        'date': '2024-01-20',
        'total': 100.50,
        'items': [
            {
                'name': 'Test Product',
                'quantity': 1,
                'price': 100.50,
                'unit': 'szt'
            }
        ]
    }
    saved_receipt = db_manager.save_receipt(receipt_data)

    # Pobranie paragonu
    receipt = db_manager.get_receipt(saved_receipt.id)

    # Sprawdzenie wyników
    assert receipt is not None
    assert receipt.id == saved_receipt.id
    assert receipt.store == 'Test Store'
    assert receipt.total == 100.50
    assert len(receipt.items) == 1


def test_receipt_not_found(db_manager):
    """Test pobierania nieistniejącego paragonu"""
    receipt = db_manager.get_receipt(999)
    assert receipt is None


def test_inventory_management(db_manager):
    """Test zarządzania stanem magazynowym"""
    # Najpierw dodajmy testowy paragon
    receipt_data = {
        'store': 'Test Store',
        'date': '2024-01-20',
        'total': 100.50,
        'items': [
            {
                'name': 'Produkt testowy 1',
                'quantity': 5,
                'price': 20.00,
                'unit': 'szt',
                'current_quantity': 5,
                'expiry_date': '2024-06-20',
                'notes': 'Notatka testowa'
            },
            {
                'name': 'Produkt testowy 2',
                'quantity': 2,
                'price': 10.25,
                'unit': 'kg',
                'current_quantity': 2,
                'expiry_date': None,
                'notes': None
            }
        ]
    }

    # Zapisz paragon
    receipt = db_manager.save_receipt(receipt_data)
    assert receipt is not None

    # Pobierz stan magazynowy
    inventory = db_manager.get_inventory_items()
    assert len(inventory) == 2

    # Sprawdź czy stany są poprawne
    first_item = inventory[0]
    assert first_item.name == 'Produkt testowy 1'
    assert first_item.current_quantity == 5

    # Zaktualizuj ilość pierwszego produktu
    success = db_manager.update_item_quantity(first_item.id, 3, "Zużyto 2 sztuki")
    assert success is True

    # Sprawdź czy aktualizacja się powiodła
    updated_inventory = db_manager.get_inventory_items()
    updated_item = next(item for item in updated_inventory if item.id == first_item.id)
    assert updated_item.current_quantity == 3
    assert "Zużyto 2 sztuki" in updated_item.notes
# Database tests