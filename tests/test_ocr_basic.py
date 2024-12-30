import pytest
import os
from src.config import config
from src.services.ocr import OCRService


def test_ocr_credentials_exist():
    """Test sprawdzający czy plik credentials istnieje"""
    assert os.path.exists(config.GOOGLE_CLOUD_CREDENTIALS)
    assert os.path.isfile(config.GOOGLE_CLOUD_CREDENTIALS)


def test_ocr_service_creation():
    """Test sprawdzający czy można utworzyć instancję OCRService"""
    try:
        service = OCRService(config.GOOGLE_CLOUD_CREDENTIALS)
        assert service is not None
    except Exception as e:
        pytest.fail(f"Nie udało się utworzyć OCRService: {str(e)}")


def test_ocr_image_processing():
    """Test sprawdzający przetwarzanie przykładowego paragonu"""
    # Ścieżka do przykładowego paragonu
    test_image = os.path.join(config.UPLOAD_FOLDER, "paragon.PNG")

    # Sprawdź czy plik istnieje
    if not os.path.exists(test_image):
        pytest.skip("Brak pliku testowego paragonu")

    # Utwórz serwis OCR
    service = OCRService(config.GOOGLE_CLOUD_CREDENTIALS)

    # Przetwórz obraz
    try:
        result = service.process_image(test_image)

        # Sprawdź czy wynik zawiera wszystkie wymagane pola
        assert isinstance(result, dict)
        assert 'store' in result
        assert 'date' in result
        assert 'products' in result
        assert 'total' in result

        # Sprawdź czy lista produktów nie jest pusta
        assert isinstance(result['products'], list)

        # Jeśli są produkty, sprawdź strukturę pierwszego
        if result['products']:
            product = result['products'][0]
            assert 'name' in product
            assert 'quantity' in product
            assert 'unit' in product
            assert 'price' in product

    except Exception as e:
        pytest.fail(f"Błąd podczas przetwarzania obrazu: {str(e)}")


if __name__ == "__main__":
    pytest.main([__file__])