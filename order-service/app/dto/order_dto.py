from pydantic import BaseModel, Field

class OrderCreateDto(BaseModel):
    product_id: str = Field(..., min_length=5)
    quantity: int = Field(..., gt=0)
