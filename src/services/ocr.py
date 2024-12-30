import re
from typing import List, Tuple
from google.cloud import vision
from pathlib import Path
from typing import Dict, Any
import logging
import pytesseract
from PIL import Image

# Konfiguracja loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self, credentials_path: str = None):
        self.credentials_path = credentials_path

    def process_image(self, image_path):
        """
        Process an image and extract text using Tesseract OCR
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            str: Extracted text from the image
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            raise RuntimeError(f"OCR processing failed: {str(e)}")

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

        # Analiza rozpoznanego tekstu
        full_text = texts[0].description
        store_name = extract_store_name(full_text)
        total = extract_total_amount(full_text)
        products = extract_products(full_text)

        return {
            'store': store_name,
            'total_amount': total,
            'products': products
        }

    except FileNotFoundError as e:
        logger.error(f"Błąd dostępu do pliku: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Błąd podczas przetwarzania obrazu: {str(e)}")
        raise Exception(f"Wystąpił błąd podczas przetwarzania paragonu: {str(e)}")


def extract_store_name(text: str) -> str:
    # Typowe słowa kluczowe dla nazw sklepów
    store_keywords = ['sp. z o.o.', 's.a.', 'sklep', 'market', 'supermarket']
    
    # Szukaj w pierwszych liniach tekstu
    first_lines = text.split('\n')[:3]
    for line in first_lines:
        line = line.strip().upper()
        if any(keyword.upper() in line for keyword in store_keywords):
            return line
        # Pierwsza linia często zawiera nazwę sklepu
        if len(line) > 3 and not any(char.isdigit() for char in line):
            return line
    
    return "Nieznany"

def extract_total_amount(text: str) -> float:
    # Szukaj wzorców kwot typu "SUMA PLN 123.45" lub "RAZEM 123,45"
    patterns = [
        r'(?:SUMA|RAZEM|TOTAL).*?(\d+[.,]\d{2})',
        r'(?:PLN|ZŁ).*?(\d+[.,]\d{2})',
        r'(\d+[.,]\d{2})(?:\s*(?:PLN|ZŁ))'
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text.upper())
        amounts = [float(m.group(1).replace(',', '.')) for m in matches]
        if amounts:
            return max(amounts)
    
    return 0.0

def extract_products(text: str) -> List[Dict[str, Any]]:
    products = []
    lines = text.split('\n')
    
    # Wzorzec dla linii z produktem: nazwa i cena
    product_pattern = r'^(.*?)\s+(\d+[.,]\d{2})\s*(?:PLN|ZŁ)?$'
    
    for line in lines:
        match = re.match(product_pattern, line.strip())
        if match:
            name, price = match.groups()
            if len(name.strip()) > 2:  # Ignoruj zbyt krótkie nazwy
                products.append({
                    'name': name.strip(),
                    'price': float(price.replace(',', '.'))
                })
    
    return products