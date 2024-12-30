from typing import Dict, List, Tuple
import re
from datetime import datetime

class ReceiptValidator:
    @staticmethod
    def validate_receipt_data(data: Dict) -> Tuple[bool, List[str]]:
        """
        Sprawdza poprawność danych paragonu.

        Returns:
            Tuple[bool, List[str]]: (czy_poprawne, lista_błędów)
        """
        errors = []

        # Sprawdzenie wymaganych pól
        required_fields = ['store', 'date', 'items', 'total']
        for field in required_fields:
            if field not in data:
                errors.append(f"Brak wymaganego pola: {field}")

        if errors:
            return False, errors

        # Walidacja daty
        try:
            datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            errors.append("Niepoprawny format daty (wymagany: YYYY-MM-DD)")

        # Walidacja total
        try:
            total = float(data['total'])
            if total < 0:
                errors.append("Suma nie może być ujemna")
        except ValueError:
            errors.append("Niepoprawny format sumy")

        # Walidacja produktów
        if not isinstance(data['items'], list):
            errors.append("Lista produktów musi być tablicą")
        else:
            for item in data['items']:
                item_errors = ReceiptValidator.validate_item(item)
                errors.extend(item_errors)

        return len(errors) == 0, errors

    @staticmethod
    def validate_item(item: Dict) -> List[str]:
        """Sprawdza poprawność pojedynczego produktu"""
        errors = []

        # Sprawdzenie wymaganych pól
        required_fields = ['name', 'quantity', 'price', 'unit']
        for field in required_fields:
            if field not in item:
                errors.append(f"Produkt - brak pola: {field}")

        if 'name' in item and not item['name'].strip():
            errors.append("Nazwa produktu nie może być pusta")

        try:
            quantity = float(item['quantity'])
            if quantity <= 0:
                errors.append("Ilość musi być większa od 0")
        except (ValueError, KeyError):
            errors.append("Niepoprawna ilość produktu")

        try:
            price = float(item['price'])
            if price < 0:
                errors.append("Cena nie może być ujemna")
        except (ValueError, KeyError):
            errors.append("Niepoprawna cena produktu")

        if 'unit' in item and item['unit'] not in ['szt', 'kg', 'g', 'l', 'ml']:
            errors.append("Niepoprawna jednostka miary")

        return errors