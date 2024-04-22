from fastapi import APIRouter, Request
from app.services.order_service import OrderService
from app.utils.kafka import consume_order_from_kafka
from app.schema_dto.order_schema import OrderCreateSchema
from app.utils.base import the_query, validate_data

# Instance
router = APIRouter()
order_service = OrderService()

@router.post("/orders")
async def create_order(request: Request, order_data: OrderCreateSchema):
 
    #data = OrderCreateSchema(**order_data.model_dump())
    
    ### manually data validate
    # dto_validate = await validate_data(data, OrderCreateSchema)
    # if dto_validate['status'] == 'invalid':
    #     return {'error': 'Validation failed', 'details': dto_validate['errors']}
    
    # Retrieve data from the request
    request_data = await the_query(request)
    data = OrderCreateSchema(**request_data)
    
    return order_service.place_order(data)


def start_order_consumer():
    while True:
        consume_order_from_kafka()
      
@router.on_event("startup")
async def startup_event():
    # Start a background task to continuously consume orders from Kafka
    import threading
    threading.Thread(target=start_order_consumer, daemon=True).start()
