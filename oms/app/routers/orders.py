import json
import uuid
from decimal import Decimal
from typing import Dict, List

import httpx
from fastapi import APIRouter, Depends, HTTPException

from .kafka import push_message
from ..database import orders
from ..dependencies import get_current_user
from ..models import TokenData, Order, OrderResponseLimited

router = APIRouter()






@router.post("/orders", dependencies=[Depends(get_current_user)])
async def place_order(order: Order, current_user: TokenData = Depends(get_current_user)):
    new_order = order.dict()
    new_order["user_id"] = current_user.username
    new_order["order_id"] = str(uuid.uuid4())

    if (current_user.username not in orders):
        orders[current_user.username] = {}

    orders[current_user.username][new_order["order_id"]] = new_order

    await push_message(new_order,"PLACE")

    return {"order_id": new_order["order_id"]}

@router.put("/orders/{order_id}", dependencies=[Depends(get_current_user)])
async def modify_order(order_id: str, updated_field: Dict, current_user: TokenData = Depends(get_current_user)):
    if(current_user.username not in orders or order_id not in orders[current_user.username]):
        raise HTTPException(status_code=404, detail="Order not found")

    orders[current_user.username][order_id]["price"] = updated_field["updated_price"]

    await push_message(orders[current_user.username][order_id],"MODIFY")

    return {"message": "Order updated successfully!"}


@router.delete("/orders/{order_id}", dependencies=[Depends(get_current_user)])
async def cancel_order(order_id: str, current_user: TokenData = Depends(get_current_user)):
    if (current_user.username not in orders or order_id not in orders[current_user.username]):
        raise HTTPException(status_code=404, detail="Order not found")
    if(orders[current_user.username][order_id]["is_active"] == False):
        return {"success": False}

    await push_message(orders[current_user.username][order_id], "CANCEL")

    del orders[current_user.username][order_id]

    return {"success": True}


@router.get("/orders/{order_id}", dependencies=[Depends(get_current_user)], response_model=OrderResponseLimited)
async def fetch_order(order_id: str, current_user: TokenData = Depends(get_current_user)):
    if (current_user.username not in orders or order_id not in orders[current_user.username]):
        raise HTTPException(status_code=404, detail="Order not found")

    return orders[current_user.username][order_id]


@router.get("/orders", dependencies=[Depends(get_current_user)], response_model=List[OrderResponseLimited])
async def fetch_all_order(current_user: TokenData = Depends(get_current_user)):
    if (current_user.username not in orders):
        raise HTTPException(status_code=404, detail="Order not found")

    return orders[current_user.username].values()





