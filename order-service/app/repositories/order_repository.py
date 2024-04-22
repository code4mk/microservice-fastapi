from app.models.order import Order
from sqlalchemy.orm import Session 

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_order(self, product_id: str, quantity: int) -> Order:
        order = Order(product_id=product_id, quantity=quantity)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

