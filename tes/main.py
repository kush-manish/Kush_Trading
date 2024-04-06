import httpx
from fastapi import FastAPI

from app.models import OrderData

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "TES"}

@app.post("/kafka/kafka-process-order")
async def process_order(order_data: OrderData):
    # Process the order here
    # For example, print the received order data
    print(f"Processing order {order_data.order_id} with description: {order_data.description}")
    # Implement your logic here

    order_data = {
        "order_id": 123,
        "description": "This is a test order"
    }

    # URL of the tes service endpoint
    mds_service_url = "http://mds:8002/kafka/kafka-process-order-trade"

    # Send a POST request to the tes service
    async with httpx.AsyncClient() as client:
        response = await client.post(mds_service_url, json=order_data)

    return {"message": "Order processed successfully", "order_id": order_data["order_id"]}

# Add CRUD endpoints here