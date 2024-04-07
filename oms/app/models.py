from typing import Optional, List

from pydantic import BaseModel, Field, condecimal

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    username: str
    email: str
    balance: int
    full_name: str
    disabled: bool

class UserInDB(User):
    hashed_password: str

class OrderData(BaseModel):
    order_id: int
    description: str
    # Add other fields as necessary

class Order(BaseModel):
    order_id: Optional[str] = None
    is_active: Optional[bool] = True
    side: int
    quantity: int
    price: condecimal(multiple_of=0.01)
    traded_quantity: Optional[int] = 0
    traded_price: Optional[int] = 0


class OrderResponseLimited(BaseModel):
    order_id: str = Field(..., alias="order_id")
    order_price: float = Field(..., alias="price")
    order_quantity: int = Field(..., alias="quantity")
    average_traded_price: Optional[float] = None
    traded_quantity: int = Field(..., alias="traded_quantity")
    order_alive: bool = Field(..., alias="is_active")

    @classmethod
    def from_order(cls, order: Order):
        order_response = OrderResponseLimited.parse_obj(order)
        if(order_response.traded_quantity!=0):
            order_response.average_traded_price = order['traded_price']/order_response.traded_quantity
        return order_response



class Trade(BaseModel):
    trade_id: Optional[str] = None
    is_active: Optional[bool] = True
    ask_order_id: str
    bid_order_id: str
    quantity: int
    price: float
    execution_timestamp: Optional[str] = None
