import uuid
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_current_user
from ..models import TokenData, Order, OrderResponseLimited

router = APIRouter()

orders = []
trades = {}


@router.post("/orders", dependencies=[Depends(get_current_user)])
async def place_order(order: Order, current_user: TokenData = Depends(get_current_user)):
    new_order = order.dict()
    new_order["user_id"] = current_user.username
    new_order["order_id"] = str(uuid.uuid4())
    orders.append(new_order)
    print(orders)
    return {"order_id": new_order["order_id"]}

@router.put("/orders/{order_id}", dependencies=[Depends(get_current_user)])
async def modify_order(order_id: str, updated_field: Dict, current_user: TokenData = Depends(get_current_user)):
    for index, existing_order in enumerate(orders):
        if existing_order["order_id"] == order_id and existing_order["user_id"] == current_user.username:
            if updated_field["updated_price"]==None:
                raise HTTPException(status_code=404, detail="updated_price key not found")
            orders[index]["price"] = updated_field["updated_price"]
            return {"message": "Order updated successfully!"}
    raise HTTPException(status_code=404, detail="Order not found")

@router.delete("/orders/{order_id}", dependencies=[Depends(get_current_user)])
async def cancel_order(order_id: str, current_user: TokenData = Depends(get_current_user)):
    for index, existing_order in enumerate(orders):
        if existing_order["order_id"] == order_id and existing_order["user_id"] == current_user.username:
            if(orders[index]["is_active"]==False):
                return {"success": False}
            del orders[index]
            return {"success": True}

    raise HTTPException(status_code=404, detail="Order not found")


@router.get("/orders/{order_id}", dependencies=[Depends(get_current_user)], response_model=List[OrderResponseLimited])
async def fetch_order(order_id: str, current_user: TokenData = Depends(get_current_user)):
    user_orders = [order for order in orders if order["user_id"] == current_user.username and order["order_id"] == order_id]
    if user_orders == []:
        raise HTTPException(status_code=404, detail="Order not found")
    return user_orders

@router.get("/orders", dependencies=[Depends(get_current_user)], response_model=List[OrderResponseLimited])
async def fetch_all_order(current_user: TokenData = Depends(get_current_user)):
    user_orders = [order for order in orders if order["user_id"] == current_user.username]
    if user_orders == []:
        raise HTTPException(status_code=404, detail="Order not found")
    return user_orders




