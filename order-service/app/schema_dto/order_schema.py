from pydantic import BaseModel, Field

class OrderCreateSchema(BaseModel):
    product_id: str = Field(..., min_length=5)
    quantity: int = Field(..., gt=0)
    
from pydantic import BaseModel

class OrderSerialized(BaseModel):
    id: int
    product_id: str
    quantity: int
    
    class Config:
        from_orm = True
        from_attributes=True

