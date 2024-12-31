class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"  # Zmień na odpowiedni URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"  # Dodaj klucz tajny, jeśli potrzebny