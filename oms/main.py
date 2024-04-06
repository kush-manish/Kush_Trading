import httpx
from fastapi import FastAPI
from fastapi import Depends

from app.dependencies import get_current_user
from app.routers import auth,orders

app = FastAPI()
app.include_router(auth.router)
app.include_router(orders.router)

@app.get("/")
async def read_root():
    return {"Hello": "OMS"}

@app.post("/create-order", dependencies=[Depends(get_current_user)])
async def create_order():
    # Simulate some work being done here
    # ...

    # Data to be sent to the tes service
    order_data = {
        "order_id": 123,
        "description": "This is a test order"
    }

    # URL of the tes service endpoint
    tes_service_url = "http://tes:8001/kafka/kafka-process-order"

    # Send a POST request to the tes service
    async with httpx.AsyncClient() as client:
        response = await client.post(tes_service_url, json=order_data)


    # Check if the request was successful
    if response.status_code == 200:
        return {"message": "Order created and sent to tes service successfully"}
    else:
        return {"message": "Failed to send order to tes service"}
