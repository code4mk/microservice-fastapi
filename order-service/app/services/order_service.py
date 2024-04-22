from app.models.order import Order
from app.repositories.order_repository import save_order
from app.utils.kafka import send_order_to_kafka
from app.utils.database import SessionLocal

def place_order(order: Order):
    db = SessionLocal()
    try:
        order = save_order(db, product_id=order.product_id, quantity=order.quantity)
        send_order_to_kafka(order)
        return order
    finally:
        db.close()
