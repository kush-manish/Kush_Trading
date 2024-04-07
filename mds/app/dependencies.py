import asyncio
from datetime import datetime

import httpx

from .database import order_book_snapshot, active_websockets


async def send_notifications(message: dict, user_id: str):
    try:
        websocket = active_websockets[user_id]
        await websocket.send_text(str(message))
    except:
        pass

async def fetch_order_book_snapshot():

    oms_service_url = "http://tes:8001/orderbook/top5"

    async with httpx.AsyncClient() as client:
        response = await client.get(oms_service_url)

        return {
            "bid": [{"price":obj.get("data",{}).get("price",-1), "qty": obj.get("data",{}).get("quantity",-1)} for obj in response.json().get("buys", [])],
            "ask": [{"price":obj.get("data",{}).get("price",-1), "qty": obj.get("data",{}).get("quantity",-1)} for obj in response.json().get("sells", [])]
        }


async def update_order_book_snapshot():
    while True:
        # Fetch the latest order book snapshot
        new_order_book_snapshot = await fetch_order_book_snapshot()
        # Update the order book snapshot
        order_book_snapshot.update(new_order_book_snapshot)
        # Wait for 0.5 seconds before fetching the next snapshot
        await asyncio.sleep(0.5)





