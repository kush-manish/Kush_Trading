from pydantic import BaseModel

class OrderData(BaseModel):
    order_id: int
    description: str
    # Add other fields as necessary
