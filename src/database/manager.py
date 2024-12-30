from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import config
from src.database.models import Base, Receipt, ReceiptItem, Category, ProductStatus
from datetime import datetime, timedelta
from typing import List, Optional


class DatabaseManager:
    def __init__(self, database_url: str = None):
        self.engine = create_engine(database_url or config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """Zwraca nową sesję bazy danych"""
        return self.Session()

    def get_categories(self) -> List[Category]:
        """Pobiera wszystkie kategorie"""
        with self.get_session() as session:
            return session.query(Category).all()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Pobiera kategorię po ID"""
        with self.get_session() as session:
            return session.query(Category).filter(Category.id == category_id).first()

    def add_receipt(self, receipt_data: dict) -> Receipt:
        """Dodaje nowy paragon z produktami"""
        with self.get_session() as session:
            try:
                receipt = Receipt(
                    store=receipt_data['store'],
                    date=receipt_data['date'],
                    total=receipt_data['total']
                )
                session.add(receipt)
                session.flush()  # Aby otrzymać ID paragonu

                # Dodanie produktów
                for item_data in receipt_data['items']:
                    item = ReceiptItem(
                        receipt_id=receipt.id,
                        name=item_data['name'],
                        quantity=item_data['quantity'],
                        price=item_data['price'],
                        unit=item_data['unit'],
                        category_id=item_data.get('category_id'),
                        expiry_date=item_data.get('expiry_date')
                    )
                    session.add(item)

                session.commit()
                return receipt
            except Exception as e:
                session.rollback()
                raise e

    def update_product_status(self, item_id: int, new_status: ProductStatus,
                              opened_date: datetime = None) -> bool:
        """Aktualizuje status produktu"""
        with self.get_session() as session:
            try:
                item = session.query(ReceiptItem).get(item_id)
                if not item:
                    return False

                item.status = new_status
                if new_status == ProductStatus.OPENED and not item.opened_date:
                    item.opened_date = opened_date or datetime.now()

                session.commit()
                return True
            except Exception as e:
                session.rollback()
                raise e

    def get_expiring_products(self, days_threshold: int = 7) -> List[ReceiptItem]:
        """Pobiera produkty z zbliżającym się terminem ważności"""
        threshold_date = datetime.now().date() + timedelta(days=days_threshold)

        with self.get_session() as session:
            return session.query(ReceiptItem).filter(
                ReceiptItem.expiry_date <= threshold_date,
                ReceiptItem.expiry_date >= datetime.now().date(),
                ReceiptItem.status != ProductStatus.USED
            ).all()

    def get_opened_products(self) -> List[ReceiptItem]:
        """Pobiera listę otwartych produktów"""
        with self.get_session() as session:
            return session.query(ReceiptItem).filter(
                ReceiptItem.status == ProductStatus.OPENED
            ).all()

    def update_product_quantity(self, item_id: int, new_quantity: float) -> bool:
        """Aktualizuje ilość produktu"""
        with self.get_session() as session:
            try:
                item = session.query(ReceiptItem).get(item_id)
                if not item:
                    return False

                item.current_quantity = new_quantity
                if new_quantity <= 0:
                    item.status = ProductStatus.USED

                session.commit()
                return True
            except Exception as e:
                session.rollback()
                raise e