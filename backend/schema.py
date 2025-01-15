from pydantic import BaseModel
from typing import List, Dict
from models import AllowedItems, OrderStatus


class OrderItemModel(BaseModel):
    name: AllowedItems
    quantity: int


class PlaceOrderRequest(BaseModel):
    items: List[OrderItemModel]


class CancelOrderRequest(BaseModel):
    order_number: int


class OrderModel(BaseModel):
    id: int
    status: OrderStatus
    items: List[OrderItemModel]


class OrderResponse(BaseModel):
    message: str
    orders: Dict[int, OrderModel]


class ProcessRequest(BaseModel):
    input: str
