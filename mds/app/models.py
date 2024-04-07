from pydantic import BaseModel

class OrderData(BaseModel):
    order_id: int
    description: str
    # Add other fields as necessary

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
