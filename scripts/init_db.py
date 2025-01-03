from src.web import create_app
from src.database.models import Category
from src.database import db


def init_categories():
    categories = [
        {"name": "Nabiał", "description": "Produkty mleczne, jaja"},
        {"name": "Pieczywo", "description": "Chleb, bułki, wypieki"},
        {"name": "Mięso", "description": "Mięso, wędliny"},
        {"name": "Warzywa", "description": "Świeże warzywa"},
        {"name": "Owoce", "description": "Świeże owoce"},
        {"name": "Napoje", "description": "Woda, soki, napoje"},
        {"name": "Chemia", "description": "Środki czystości"},
        {"name": "Przekąski", "description": "Słodycze, przekąski słone"}
    ]

    for cat_data in categories:
        # Sprawdź czy kategoria już istnieje
        if not Category.query.filter_by(name=cat_data["name"]).first():
            category = Category(**cat_data)
            db.session.add(category)

    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        init_categories()
        print("Kategorie zostały dodane do bazy danych.")