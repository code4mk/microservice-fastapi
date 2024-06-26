from app.models.order import Order
from app.repositories.order_repository import OrderRepository
from app.utils.database import SessionLocal
from app.schema_dto.order_schema import OrderCreateSchema
from app.utils.kafka import KafkaService

class OrderService:
    def __init__(self):
        self.db = SessionLocal()
        self.order_repository = OrderRepository(self.db)
        self.kafka_service = KafkaService()

    def place_order(self, order: OrderCreateSchema):
        try:
            saved_order = self.order_repository.save_order(product_id=order.product_id, quantity=order.quantity)
            data =  saved_order.as_dict()
            self.kafka_service.produce_to_kafka(topic='order_topic', data=data)
            return data
        finally:
            self.db.close()
            
    def s_get_order(self, request):
        data = self.order_repository.get_orders(request)
        return data
    
    def s_get_order_by_id(self, request, id):
        data = self.order_repository.get_order_by_id(request, id)
        return data
