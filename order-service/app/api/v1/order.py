from fastapi import APIRouter, Request
from app.models.order import Order
from app.services.order_service import OrderService
from app.utils.kafka import consume_order_from_kafka
from app.dto.order_dto import OrderCreateDto
from pydantic import ValidationError
from app.utils.base import the_query, validate_data

router = APIRouter()
order_service = OrderService()

@router.post("/orders")
async def create_order(request: Request):
    # Retrieve data from the request
    data = await the_query(request)
    
    # Validate the data
    dto_validate = await validate_data(data, OrderCreateDto)
    if dto_validate['status'] == 'invalid':
        return {'error': 'Validation failed', 'details': dto_validate['errors']}
    
    order = Order(**data)
    return order_service.place_order(order)

def start_order_consumer():
    while True:
        consume_order_from_kafka()
      
@router.on_event("startup")
async def startup_event():
    # Start a background task to continuously consume orders from Kafka
    import threading
    threading.Thread(target=start_order_consumer, daemon=True).start()
