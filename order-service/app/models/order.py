# app/models/order.py

from pydantic import BaseModel

class Order(BaseModel):
    id: int
    product_id: int
    quantity: int
    # Add other order fields as needed
