import os
from pathlib import Path
from typing import List, Dict
import logging
from datetime import datetime


def setup_logging():
    """Konfiguruje system logowania"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )


def ensure_directories():
    """Tworzy wymagane katalogi jeśli nie istnieją"""
    directories = ['data', 'data/receipts', 'logs']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def format_price(price: float) -> str:
    """Formatuje cenę do wyświetlenia"""
    return f"{price:.2f} zł"


def parse_date(date_str: str) -> datetime:
    """Parsuje datę z różnych formatów"""
    formats = ['%Y-%m-%d', '%d-%m-%Y', '%d.%m.%Y']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Nie można sparsować daty: {date_str}")


def clean_filename(filename: str) -> str:
    """Czyści nazwę pliku z niedozwolonych znaków"""
    return "".join(c for c in filename if c.isalnum() or c in "._- ")
# Helper functions