import httpx
from fastapi import FastAPI
from fastapi import Depends

from app.dependencies import get_current_user
from app.routers import auth,orders,kafka,trades


app = FastAPI()
app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(kafka.router)
app.include_router(trades.router)

@app.get("/")
async def read_root():
    return {"Hello": "OMS"}


