import uuid
from datetime import datetime
import httpx
from fastapi import FastAPI
from app.models import OrderData, order_with_price
import heapq

from app.database import sell_orders,buy_orders
from app.routers import kafka

# Min heap for buy orders and max heap for sell orders



app = FastAPI()
app.include_router(kafka.router)

@app.get("/")
async def read_root():
    return {"Hello": "TES"}






