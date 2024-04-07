import asyncio
from datetime import datetime
from typing import List, Dict

from fastapi import FastAPI, WebSocket, Depends, BackgroundTasks
from fastapi.responses import HTMLResponse

from app.routers.auth import get_current_user

app = FastAPI()

active_websockets: List[WebSocket] = {}

@app.get("/")
async def read_root():
    return {"Hello": 0}


async def send_notifications(message: dict, user_id: str):
    try:
        websocket = active_websockets[user_id]
        await websocket.send_text(str(message))
    except:
        pass


order_book_snapshot: Dict[str, List[Dict[str, float]]] = {
    "bid": [],
    "ask": []
}

async def fetch_order_book_snapshot():

    return {
        "fatch_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "bid": [
            {"price": 100.0, "quantity": 10},
            {"price": 99.5, "quantity": 15},
            {"price": 99.0, "quantity": 20},
            {"price": 98.5, "quantity": 25},
            {"price": 98.0, "quantity": 30}
        ],
        "ask": [
            {"price": 101.0, "quantity": 10},
            {"price": 101.5, "quantity": 15},
            {"price": 102.0, "quantity": 20},
            {"price": 102.5, "quantity": 25},
            {"price": 103.0, "quantity": 30}
        ]
    }


async def update_order_book_snapshot():
    while True:
        # Fetch the latest order book snapshot
        new_order_book_snapshot = await fetch_order_book_snapshot()
        # Update the order book snapshot
        order_book_snapshot.update(new_order_book_snapshot)
        # Wait for 0.5 seconds before fetching the next snapshot
        await asyncio.sleep(0.5)

@app.on_event("startup")
async def startup_event():
    # Start the background task to update the order book snapshot
    asyncio.create_task(update_order_book_snapshot())


@app.post("/kafka/kafka-order-trade-happened")
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



@app.websocket("/ws/orderbook")
async def send_order_book_snapshot(websocket: WebSocket, user: dict = Depends(get_current_user)):

    if not user:
        # If user is False, it means token validation failed
        # You can choose to send a message to the client before closing the connection
        await websocket.send_text("Authentication failed.")
        await websocket.close(code=1008)
        return  # Exit the function to prevent further execution

    await websocket.accept()
    while True:
        # Send order book snapshot
        await websocket.send_json(order_book_snapshot)
        # Wait for 1 second before sending the next snapshot
        await asyncio.sleep(1)

@app.websocket("/ws/trades")
async def websocket_endpoint(websocket: WebSocket, user: dict = Depends(get_current_user)):
    if not user:
        # If user is False, it means token validation failed
        # You can choose to send a message to the client before closing the connection
        await websocket.send_text("Authentication failed.")
        await websocket.close(code=1008)
        return  # Exit the function to prevent further execution

    active_websockets[user.username] = websocket

    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}, from: {user.username}")
