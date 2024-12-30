import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.web.app import app
from src.database.manager import DatabaseManager
from pathlib import Path
import json
from io import BytesIO


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = Path('test_uploads')
    with app.test_client() as client:
        yield client
    # Cleanup
    if os.path.exists('test_uploads'):
        for file in Path('test_uploads').glob('*'):
            file.unlink()
        Path('test_uploads').rmdir()


@pytest.fixture
def sample_receipt_data():
    return {
        'store': 'Test Store',
        'date': '2024-01-20',
        'products': [
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
        ],
        'total': 100.50
    }


def test_index(client):
    """Test strony głównej"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Smart Zapasy' in response.data


def test_upload_no_file(client):
    """Test uploadu bez pliku"""
    response = client.post('/upload')
    assert response.status_code == 302  # Redirect


def test_upload_invalid_file(client):
    """Test uploadu nieprawidłowego pliku"""
    data = {
        'receipt': (BytesIO(b'invalid file content'), 'test.txt')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 302  # Redirect


def test_upload_valid_file(client):
    """Test uploadu prawidłowego pliku"""
    # Tworzenie przykładowego obrazu PNG
    from PIL import Image
    import io

    img = Image.new('RGB', (100, 100), color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    data = {
        'receipt': (BytesIO(img_byte_arr), 'test.png')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'Weryfikacja' in response.data


def test_save_receipt(client, sample_receipt_data):
    """Test zapisywania paragonu"""
    response = client.post('/save',
                           data=json.dumps(sample_receipt_data),
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True


def test_save_receipt_invalid_data(client):
    """Test zapisywania paragonu z nieprawidłowymi danymi"""
    invalid_data = {
        'store': 'Test Store',
        # brak wymaganych pól
    }
    response = client.post('/save',
                           data=json.dumps(invalid_data),
                           content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False


def test_list_receipts(client):
    """Test listy paragonów"""
    response = client.get('/receipts')
    assert response.status_code == 200
    assert b'Lista paragon' in response.data


def test_view_receipt(client, sample_receipt_data):
    """Test widoku szczegółów paragonu"""
    # Najpierw zapisz paragon
    response = client.post('/save',
                           data=json.dumps(sample_receipt_data),
                           content_type='application/json')
    data = json.loads(response.data)
    receipt_id = data['receipt_id']

    # Następnie sprawdź widok szczegółów
    response = client.get(f'/receipt/{receipt_id}')
    assert response.status_code == 200
    assert b'Test Store' in response.data


def test_view_nonexistent_receipt(client):
    """Test widoku nieistniejącego paragonu"""
    response = client.get('/receipt/999')
    assert response.status_code == 302  # Redirect
# API tests