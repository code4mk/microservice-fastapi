 
from pydantic import BaseModel

class order_lists_serializer(BaseModel):
    product_id: str
    quantity: int
    
    class Config:
        from_orm = True
        from_attributes=True