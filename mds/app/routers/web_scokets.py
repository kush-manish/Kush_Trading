
import asyncio
from fastapi import  WebSocket, Depends, APIRouter

from ..database import active_websockets, order_book_snapshot
from .auth import get_current_user

router = APIRouter()

@router.websocket("/ws/orderbook")
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
