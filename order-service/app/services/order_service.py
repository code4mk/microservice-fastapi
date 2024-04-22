# app/services/order_service.py

from app.models.order import Order
from app.repositories.order_repository import save_order
from app.utils.kafka import send_order_to_kafka

def place_order(order: Order):
    saved_order = save_order(order)
    send_order_to_kafka(saved_order)
    return saved_order
