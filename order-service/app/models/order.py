from sqlalchemy import Column, Integer, String
from app.utils.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    quantity = Column(Integer, index=True)
    
    # id, customer_id ,items, total_price, shipping_address, status

