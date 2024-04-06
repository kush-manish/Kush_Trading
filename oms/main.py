import httpx
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status

from app.models import OrderData
from app.auth import authenticate_user, get_current_user
from app.my_database import fake_users_db
from app import auth

app = FastAPI()
app.include_router(auth.router)

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
# Add CRUD endpoints here

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # In a real application, return a secure token here
    return {"access_token": user["username"], "token_type": "bearer"}