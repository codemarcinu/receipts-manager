import os
from pathlib import Path
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()

class Config:
    # Podstawowa konfiguracja
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = 'dev'
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'

    # Konfiguracja bazy danych
    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/data/zakupy.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/receipts.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATE_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migrations')

    # Konfiguracja katalogów
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    RECEIPTS_FOLDER = BASE_DIR / 'data' / 'receipts'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit

    # Konfiguracja logowania
    LOG_FILE = BASE_DIR / 'logs' / 'smart_zapasy.log'
    LOG_LEVEL = 'INFO'

    # Google Cloud Vision API
    GOOGLE_CLOUD_CREDENTIALS = BASE_DIR / 'config' / 'credentials' / 'google-cloud-vision.json'

    def __init__(self):
        # Tworzenie wymaganych katalogów
        for path in [self.UPLOAD_FOLDER, self.RECEIPTS_FOLDER, self.LOG_FILE.parent]:
            path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def init_app(app):
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

config = Config()