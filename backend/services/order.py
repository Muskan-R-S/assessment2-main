from sqlalchemy.orm import Session
from models import Order, OrderItem, AllowedItems, OrderStatus
from fastapi import HTTPException


def place_order(db: Session, items: list):
    # Validate items
    for item in items:
        if item.get("name", "") not in AllowedItems.__members__:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid item: {item.get('name')}",
            )

    # Create a new order
    new_order = Order(status=OrderStatus.active)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Add order items
    for item in items:
        order_item = OrderItem(
            order_id=new_order.id,
            name=item["name"],
            quantity=item["quantity"],
        )
        db.add(order_item)
    db.commit()

    return new_order.id


def cancel_order(db: Session, order_number: int):
    # Validate order number
    order = db.query(Order).filter(Order.id == order_number).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order #{order_number} not found.")

    # Mark the order as "cancelled"
    order.status = OrderStatus.cancelled
    db.commit()

    return order_number


def get_all_orders(db: Session):
    # Fetch all orders and their items
    all_orders = {}
    for order in db.query(Order).all():
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        all_orders[order.id] = {
            "id": order.id,
            "status": order.status,
            "items": [{"name": item.name, "quantity": item.quantity} for item in items],
        }
    return all_orders
