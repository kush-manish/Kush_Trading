from ..dependencies import send_notifications
from fastapi import FastAPI, WebSocket, Depends, BackgroundTasks, APIRouter

router = APIRouter()
@router.post("/kafka/kafka-order-trade-happened")
async def order_trade_happened(trade_data: dict):
    # Process the order here
    # For example, print the received order data

    for key in trade_data.keys():
        trade = trade_data[key]
        await send_notifications({
            "message": "successfully trade",
            "order_id":trade['bid_order']['order_id'],
            "qty":trade['trade_quantity'],
            "price:":trade['price'],
            "timestamp":trade['timestamp'],

        }, trade['bid_order']['user_id'])
        await send_notifications({
            "message": "successfully trade",
            "order_id": trade['ask_order']['order_id'],
            "qty": trade['trade_quantity'],
            "price:": trade['price'],
            "timestamp": trade['timestamp'],

        }, trade['ask_order']['user_id'])


    return None