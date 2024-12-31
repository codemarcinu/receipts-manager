import os
from pathlib import Path

class Config:
    # Get the base directory of the project
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Ensure data directory exists
    DATA_DIR = BASE_DIR / 'data'
    DATA_DIR.mkdir(exist_ok=True)
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATA_DIR}/receipts.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-123')
    
    @staticmethod
    def init_app(app):
        os.makedirs(app.config['DATA_DIR'], exist_ok=True)

config = Config()