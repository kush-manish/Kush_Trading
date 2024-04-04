from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from dependencies import oauth2_scheme, ALGORITHM, SECRET_KEY, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token
from routers.auth import get_current_user
from schemas import TokenData, User, Token, Order

router = APIRouter()

orders = []


@router.post("/orders", dependencies=[Depends(get_current_user)])
async def create_order(order: Order, current_user: TokenData = Depends(get_current_user)):
    new_order = order.dict()
    new_order["user_id"] = current_user.username
    new_order["order_id"] = int(datetime.now().timestamp())
    orders.append(new_order)
    return {"message": "Order created successfully!"}

@router.get("/orders", dependencies=[Depends(get_current_user)])
async def get_orders(current_user: TokenData = Depends(get_current_user)):
    user_orders = [order for order in orders if order["user_id"] == current_user.username]
    return user_orders

@router.put("/orders/{order_id}", dependencies=[Depends(get_current_user)])
async def update_order(order_id: int, order: Order, current_user: TokenData = Depends(get_current_user)):
    for index, existing_order in enumerate(orders):
        if existing_order["order_id"] == order_id and existing_order["user_id"] == current_user.username:
            new_order = order.dict()
            new_order["user_id"] = current_user.username
            new_order["order_id"] = order_id
            orders[index] = new_order
            return {"message": "Order updated successfully!"}
    raise HTTPException(status_code=404, detail="Order not found")

@router.delete("/orders/{order_id}", dependencies=[Depends(get_current_user)])
async def delete_order(order_id: int, current_user: TokenData = Depends(get_current_user)):
    for index, existing_order in enumerate(orders):
        if existing_order["order_id"] == order_id and existing_order["user_id"] == current_user.username:
            del orders[index]
            return {"message": "Order deleted successfully!"}
    raise HTTPException(status_code=404, detail="Order not found")




