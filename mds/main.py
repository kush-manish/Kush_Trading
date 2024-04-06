from fastapi import FastAPI


from app.models import OrderData
from app.auth import authenticate_user

app = FastAPI()

count = {}
@app.get("/")
async def read_root():
    return {"Hello": count}

@app.post("/kafka/kafka-process-order-trade")
async def process_order_trade(order_data: OrderData):
    # Process the order here
    # For example, print the received order data
    count['X'] = 1;
    print(count)
    print(f"Processing order & trade {order_data.order_id} ")
    # Implement your logic here

    return {"message": "Order Trade processed successfully", "order_id": order_data.order_id}


# Add CRUD endpoints here