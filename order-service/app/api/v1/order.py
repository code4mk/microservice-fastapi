from fastapi import APIRouter, Request
from app.models.order import Order
from app.services.order_service import OrderService
from app.utils.kafka import consume_order_from_kafka
from app.dto.order_dto import OrderCreateDto
from pydantic import ValidationError


router = APIRouter()
order_service = OrderService()

@router.post("/orders")
async def create_order(request: Request):
    data = await request.json() if request.headers.get("Content-Type") == "application/json" else await request.form()
    try:
        a = OrderCreateDto(**data)
        order = Order(**data)
        return order_service.place_order(order)
    except ValidationError as e:
        return{'error': e.errors()}

def start_order_consumer():
    while True:
        consume_order_from_kafka()
      
@router.on_event("startup")
async def startup_event():
    # Start a background task to continuously consume orders from Kafka
    import threading
    threading.Thread(target=start_order_consumer, daemon=True).start()
