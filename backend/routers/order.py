from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal
from schema import OrderResponse, OrderItemModel, ProcessRequest, OrderModel
from utils import get_openai_response
from services import place_order, cancel_order, get_all_orders
from typing import Dict, List

router = APIRouter()


@router.post("/process", response_model=OrderResponse)
async def process_user_input(process_request: ProcessRequest):
    try:
        user_input = process_request.input
        ai_response = get_openai_response(user_input)
        tool_calls = ai_response.choices[0].message.tool_calls

        if not tool_calls:
            raise HTTPException(
                status_code=400, detail="Unable to interpret user input."
            )

        for tool_call in tool_calls:

            if not tool_call.function:
                raise HTTPException(
                    status_code=400, detail="Unable to interpret user input."
                )

            function_name = tool_call.function.name
            import json

            arguments = json.loads(tool_call.function.arguments)

            with SessionLocal() as db:
                if function_name == "place_order":
                    items = arguments.get("items", [])
                    order_id = place_order(db, items)
                    response_message = f"Order #{order_id} placed successfully."

                elif function_name == "cancel_order":
                    order_number = int(arguments.get("id"))
                    canceled_order_number = cancel_order(db, order_number)
                    response_message = (
                        f"Order #{canceled_order_number} canceled successfully."
                    )

                else:
                    raise HTTPException(
                        status_code=400, detail="Unknown function call."
                    )

        # Fetch all current orders
        all_orders = get_all_orders(db)

        return OrderResponse(message=response_message, orders=all_orders)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orders", response_model=Dict[int, OrderModel])
async def get_orders():
    with SessionLocal() as db:
        all_orders = get_all_orders(db)
    return all_orders
