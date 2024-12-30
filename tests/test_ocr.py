import pytest
from src.services.ocr import OCRService
from pathlib import Path
from unittest.mock import Mock, patch
import os


@pytest.fixture
def mock_vision_client():
    with patch('src.services.ocr.vision.ImageAnnotatorClient') as mock:
        yield mock


@pytest.fixture
def ocr_service(mock_vision_client):
    return OCRService("dummy_path")


def test_extract_store():
    """Test wyciągania nazwy sklepu z tekstu"""
    ocr = OCRService("dummy_path")
    sample_text = """BIEDRONKA
    ul. Przykładowa 123
    01-234 Warszawa
    2024-01-20"""

    assert ocr._extract_store(sample_text) == "BIEDRONKA"


def test_extract_date():
    """Test wyciągania daty z tekstu"""
    ocr = OCRService("dummy_path")
    sample_text = """BIEDRONKA
    Data: 2024-01-20"""

    result = ocr._extract_date(sample_text)
    assert result is not None
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 20


def test_parse_product_line():
    """Test parsowania linii z produktem"""
    ocr = OCRService("dummy_path")
    sample_lines = [
        "Chleb 3.99",
        "Masło 200g 7.99",
        "Mleko 1l 4.50",
        "Jabłka 1.5kg 7.49"
    ]

    expected_results = [
        {'name': 'Chleb', 'quantity': 1, 'unit': 'szt', 'price': 3.99},
        {'name': 'Masło', 'quantity': 200, 'unit': 'g', 'price': 7.99},
        {'name': 'Mleko', 'quantity': 1, 'unit': 'l', 'price': 4.50},
        {'name': 'Jabłka', 'quantity': 1.5, 'unit': 'kg', 'price': 7.49}
    ]

    for line, expected in zip(sample_lines, expected_results):
        result = ocr._parse_product_line(line)
        assert result is not None
        assert result['name'] == expected['name']
        assert result['price'] == expected['price']


@pytest.mark.integration
def test_process_image(ocr_service, mock_vision_client):
    """Test przetwarzania całego paragonu"""
    # Przygotowanie mocka odpowiedzi z Google Vision
    mock_response = Mock()
    mock_response.text_annotations = [Mock(description="""
    BIEDRONKA
    ul. Przykładowa 123
    2024-01-20

    Chleb 3.99
    Masło 200g 7.99
    Mleko 1l 4.50

    SUMA PLN 16.48
    """)]
    mock_response.error = Mock(message=None)

    mock_vision_client.return_value.text_detection.return_value = mock_response

    # Wykonanie testu
    result = ocr_service.process_image("dummy_path")

    # Sprawdzenie rezultatów
    assert result is not None
    assert result['store'] == "BIEDRONKA"
    assert result['date'] == "2024-01-20"
    assert len(result['products']) == 3
    assert result['total'] == 16.48
# OCR tests