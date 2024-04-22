from app.models.order import Order
from sqlalchemy.orm import Session 

def save_order(db: Session, product_id: str, quantity: int):
    order = Order(product_id=product_id, quantity=quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

    
    
