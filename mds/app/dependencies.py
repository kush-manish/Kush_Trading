import asyncio
from datetime import datetime

from .database import order_book_snapshot, active_websockets


async def send_notifications(message: dict, user_id: str):
    try:
        websocket = active_websockets[user_id]
        await websocket.send_text(str(message))
    except:
        pass
async def update_order_book_snapshot():
    while True:
        # Fetch the latest order book snapshot
        new_order_book_snapshot = await fetch_order_book_snapshot()
        # Update the order book snapshot
        order_book_snapshot.update(new_order_book_snapshot)
        # Wait for 0.5 seconds before fetching the next snapshot
        await asyncio.sleep(0.5)

async def fetch_order_book_snapshot():

    return {
        "updated": datetime.utcnow().isoformat(),
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




