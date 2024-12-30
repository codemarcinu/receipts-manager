"""
Moduł obsługi błędów dla aplikacji Flask.
Definiuje handlery dla różnych kodów błędów HTTP.
"""
from flask import Blueprint, render_template
from src.database import db

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found_error(error):
    """Obsługa błędu 404 - Nie znaleziono zasobu."""
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def internal_error(error):
    """
    Obsługa błędu 500 - Wewnętrzny błąd serwera.
    W przypadku błędu wykonuje rollback sesji bazy danych.
    """
    db.session.rollback()
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(403)
def forbidden_error(error):
    """Obsługa błędu 403 - Brak dostępu."""
    return render_template('errors/403.html'), 403