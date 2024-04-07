import uuid
from datetime import datetime
import httpx
from fastapi import FastAPI
from app.models import OrderData, order_with_price
import heapq

from app.database import sell_orders,buy_orders

from app.dependencies import match_order, delete_order

# Min heap for buy orders and max heap for sell orders



app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "TES"}


@app.post("/kafka/kafka-process-order")
async def process_order(order_data: dict):

    #print(f"Processing data {order_data}")

    if order_data['type'] == 'PLACE':
        await match_order(order_data['data'])

    elif order_data['type'] == 'MODIFY':
        order_old = delete_order(order_data['data'])
        if (order_old != None):
            order_old['price'] = order_data['data']['price']
            await match_order(order_old)

    elif order_data['type'] == 'CANCEL':
        delete_order(order_data['data'])

    print("---------")
    print("buy",[k.data for k in buy_orders])
    print()
    print("sell",[s.data for s in sell_orders])
    print("---------")

    return None



