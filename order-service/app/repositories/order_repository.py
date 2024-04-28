from app.models.order import Order
from sqlalchemy.orm import Session 
from fastapi import Request
from app.common.paginate import paginate
from app.serializers.order_serializer import order_lists_serializer
from app.utils.base import parse_sort_params

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_order(self, product_id: str, quantity: int) -> Order:
        order = Order(product_id=product_id, quantity=quantity)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_orders(self, request: Request):
        orders = self.db.query(Order)
        
        sort_params = request.query_params.get("sort")
        if sort_params:
            ordering = parse_sort_params(sort_params)
            orders = orders.order_by(*ordering)
            
        return paginate(request, orders, serilizer=order_lists_serializer, wrap='orders')
    
    def get_order_by_id(self, request: Request, id: int):
        order = self.db.query(Order).filter_by(id=id).first()
        return order