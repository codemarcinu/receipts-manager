from sqlalchemy import create_engine, text
from src.config import config
from src.database.models import Base, Category, DEFAULT_CATEGORIES
from sqlalchemy.orm import sessionmaker


def init_db():
    """Inicjalizacja bazy danych"""
    engine = create_engine(config.DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine


def add_default_categories(session):
    """Dodawanie domyślnych kategorii"""
    existing_categories = session.query(Category).all()
    existing_names = {category.name for category in existing_categories}

    categories_to_add = []
    for name, description in DEFAULT_CATEGORIES:
        if name not in existing_names:
            categories_to_add.append(Category(name=name, description=description))

    if categories_to_add:
        session.add_all(categories_to_add)
        session.commit()
        print(f"Dodano {len(categories_to_add)} nowych kategorii")
    else:
        print("Wszystkie kategorie już istnieją")


def add_status_column():
    """Dodanie kolumny status do tabeli receipt_items"""
    engine = create_engine(config.DATABASE_URL)

    try:
        with engine.connect() as conn:
            conn.execute(text("""
                ALTER TABLE receipt_items 
                ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'nowy',
                ADD COLUMN IF NOT EXISTS opened_date DATE,
                ADD COLUMN IF NOT EXISTS category_id INTEGER 
                    REFERENCES categories(id) ON DELETE SET NULL
            """))
            conn.commit()
            print("Dodano nowe kolumny do tabeli receipt_items")
    except Exception as e:
        print(f"Błąd podczas dodawania kolumn: {str(e)}")


def run_migrations():
    """Uruchomienie wszystkich migracji"""
    try:
        print("Rozpoczynanie migracji bazy danych...")

        # Inicjalizacja bazy i utworzenie tabel
        engine = init_db()
        print("Utworzono/zaktualizowano strukturę bazy danych")

        # Utworzenie sesji
        Session = sessionmaker(bind=engine)
        session = Session()

        # Dodanie domyślnych kategorii
        add_default_categories(session)

        # Dodanie kolumn do istniejącej tabeli
        add_status_column()

        print("Migracja zakończona pomyślnie")

    except Exception as e:
        print(f"Wystąpił błąd podczas migracji: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    run_migrations()