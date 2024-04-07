from typing import List

import httpx
from fastapi import APIRouter, Depends, HTTPException


from ..models import TokenData, Order, OrderResponseLimited
from ..database import orders, trades

router = APIRouter()

async def push_message(order_data: Order, type: str):
    # URL of the tes service endpoint
    tes_service_url = "http://tes:8001/kafka/kafka-process-order"

    order_data['price'] = float(order_data['price'])

    async with httpx.AsyncClient() as client:
        response = await client.post(tes_service_url, json={"data": order_data, "type": type})

@router.post("/kafka/kafka-trade-done")
async def trade_done(order_data: dict):
    # Process the order here
    # For example, print the received order data
    for trade_id in order_data:
        trade = order_data[trade_id]

        trades[trade_id] = {
            "trade_id":trade_id,
            "execution_timestamp":order_data[trade_id]["timestamp"],
            "price":order_data[trade_id]["price"],
            "quantity":order_data[trade_id]["trade_quantity"],
            "bid_order_id":order_data[trade_id]["bid_order"]["order_id"],
            "ask_order_id": order_data[trade_id]["ask_order"]["order_id"]
        }


        # bid
        bid_user_id = trade["bid_order"]['user_id']
        bid_order_id = trade["bid_order"]['order_id']
        trade_quantity = orders[bid_user_id][bid_order_id]['quantity'] - trade["bid_order"]['quantity']
        orders[bid_user_id][bid_order_id]['traded_quantity'] += trade_quantity
        orders[bid_user_id][bid_order_id]['traded_price'] += trade_quantity*order_data[trade_id]["price"]
        orders[bid_user_id][bid_order_id]['quantity'] = trade["bid_order"]['quantity']
        if(trade["bid_order"]['quantity'] == 0):
            orders[bid_user_id][bid_order_id]['is_active'] = False

        # ask
        ask_user_id = trade["ask_order"]['user_id']
        ask_order_id = trade["ask_order"]['order_id']
        trade_quantity = orders[ask_user_id][ask_order_id]['quantity'] - trade["ask_order"]['quantity']
        orders[ask_user_id][ask_order_id]['traded_quantity'] += trade_quantity
        orders[ask_user_id][ask_order_id]['traded_price'] += trade_quantity * order_data[trade_id]["price"]
        orders[ask_user_id][ask_order_id]['quantity'] = trade["ask_order"]['quantity']
        if (trade["ask_order"]['quantity'] == 0):
            orders[ask_user_id][ask_order_id]['is_active'] = False

    return None
