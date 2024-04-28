from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from app.services.order_service import OrderService
from app.schema_dto.order_schema import OrderCreateSchema
from app.utils.base import the_query, validate_data
from app.utils.kafka import KafkaService
from app.schema_dto.order_schema import OrderCreateSchema
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/order-service")

order_service = OrderService()
kafka_service = KafkaService()


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
    
    output = order_service.place_order(data)
    return JSONResponse(content=output, status_code=status.HTTP_200_OK)

@router.get("/orders/")
async def get_orders(request: Request):
    data = order_service.s_get_order(request)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

@router.get("/orders/{id}")
async def get_orders(request: Request, id: int):
    data = order_service.s_get_order_by_id(request, id)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

def start_order_consumer():
    while True:
        kafka_service.consume_from_kafka(topic='order_topic')
      
@router.on_event("startup")
async def startup_event():
    # Start a background task to continuously consume orders from Kafka
    import threading
    threading.Thread(target=start_order_consumer, daemon=True).start()
