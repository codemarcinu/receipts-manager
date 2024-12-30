from google.cloud import vision
from pathlib import Path
from typing import Dict, Any
import logging

# Konfiguracja loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_receipt_image(image_path: str) -> Dict[str, Any]:
    """
    Przetwarza zdjęcie paragonu używając Google Cloud Vision API.

    Args:
        image_path: Ścieżka do pliku ze zdjęciem paragonu

    Returns:
        Dict zawierający wyekstrahowane dane z paragonu (sklep, data, produkty, etc.)

    Raises:
        FileNotFoundError: Gdy plik nie istnieje
        Exception: Dla innych błędów podczas przetwarzania
    """
    try:
        # Sprawdzenie czy plik istnieje
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Nie znaleziono pliku: {image_path}")

        # Inicjalizacja klienta Vision API
        client = vision.ImageAnnotatorClient()

        # Wczytanie obrazu
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Wykonanie rozpoznawania tekstu
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if not texts:
            logger.warning("Nie wykryto tekstu na obrazie")
            return {
                'store': 'Nieznany',
                'total_amount': 0.0,
                'products': []
            }

        # TODO: Implementacja szczegółowej analizy tekstu
        # Na razie zwracamy podstawowe dane
        return {
            'store': 'Nieznany',  # TODO: Wykrywanie nazwy sklepu
            'total_amount': 0.0,  # TODO: Wykrywanie kwoty
            'products': []  # TODO: Wykrywanie produktów
        }

    except FileNotFoundError as e:
        logger.error(f"Błąd dostępu do pliku: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Błąd podczas przetwarzania obrazu: {str(e)}")
        raise Exception(f"Wystąpił błąd podczas przetwarzania paragonu: {str(e)}")


def extract_store_name(text: str) -> str:
    """
    Próbuje wyekstrahować nazwę sklepu z tekstu paragonu.
    TODO: Implementacja
    """
    return "Nieznany"


def extract_total_amount(text: str) -> float:
    """
    Próbuje wyekstrahować kwotę całkowitą z tekstu paragonu.
    TODO: Implementacja
    """
    return 0.0


def extract_products(text: str) -> list:
    """
    Próbuje wyekstrahować listę produktów z tekstu paragonu.
    TODO: Implementacja
    """
    return []