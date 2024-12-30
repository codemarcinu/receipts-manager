import os
from pathlib import Path


class Config:
    # Podstawowa konfiguracja
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    DEBUG = os.environ.get('FLASK_DEBUG', False)

    # Konfiguracja bazy danych
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATABASE_PATH = BASE_DIR / 'data' / 'zakupy.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_URL = os.environ.get('DATABASE_URL', "sqlite:///development.db")

    # Konfiguracja uploadów
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'uploads'
    RECEIPTS_FOLDER = BASE_DIR / 'data' / 'receipts'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit

    # Konfiguracja logowania
    LOG_FILE = BASE_DIR / 'logs' / 'smart_zapasy.log'
    LOG_LEVEL = 'INFO'

    # Google Cloud Vision API
    GOOGLE_CLOUD_CREDENTIALS = BASE_DIR / 'config' / 'credentials' / 'google-cloud-vision.json'

    def __init__(self):
        # Upewnij się, że wymagane katalogi istnieją
        self.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        self.RECEIPTS_FOLDER.mkdir(parents=True, exist_ok=True)
        Path(self.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

config = Config()