
from fastapi import FastAPI

import heapq

from app.database import sell_orders,buy_orders

from app.dependencies import match_order, delete_order


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "TES"}


@app.get("/orderbook/top5")
async def process_order():
    return {"buys": heapq.nlargest(5,buy_orders), "sells": heapq.nsmallest(5,sell_orders)}

@app.post("/kafka/kafka-process-order")
async def process_order(order_data: dict):

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



