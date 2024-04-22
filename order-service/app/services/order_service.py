from app.models.order import Order
from app.repositories.order_repository import OrderRepository
from app.utils.kafka import send_order_to_kafka
from app.utils.database import SessionLocal
from app.schema_dto.order_schema import OrderCreateSchema

class OrderService:
    def __init__(self):
        self.db = SessionLocal()
        self.order_repository = OrderRepository(self.db)

    def place_order(self, order: OrderCreateSchema):
        try:
            saved_order = self.order_repository.save_order(product_id=order.product_id, quantity=order.quantity)
            send_order_to_kafka(saved_order)
            return saved_order
        finally:
            self.db.close()

