import asyncio
from datetime import datetime
from typing import List, Dict

from fastapi import FastAPI, WebSocket, Depends, BackgroundTasks
from fastapi.responses import HTMLResponse

from app.routers.auth import get_current_user
from app.database import active_websockets
from app.dependencies import send_notifications, update_order_book_snapshot
from app.routers import kafka, web_scokets

app = FastAPI()
app.include_router(kafka.router)
app.include_router(web_scokets.router)
@app.get("/")
async def read_root():
    return {"Hello": 0}

@app.on_event("startup")
async def startup_event():
    # Start the background task to update the order book snapshot
    asyncio.create_task(update_order_book_snapshot())


