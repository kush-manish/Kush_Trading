
import asyncio
from datetime import datetime
from typing import List, Dict

from fastapi import FastAPI, WebSocket, Depends, BackgroundTasks, APIRouter
from fastapi.responses import HTMLResponse

from ..database import active_websockets
from .auth import get_current_user

router = APIRouter()

@router.websocket("/ws/orderbook")
async def send_order_book_snapshot(websocket: WebSocket, user: dict = Depends(get_current_user)):
    order_book_snapshot = {

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

@router.websocket("/ws/trades")
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
