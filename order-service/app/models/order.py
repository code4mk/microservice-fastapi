from sqlalchemy import Column, Integer, String
from app.utils.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    quantity = Column(Integer, index=True)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

