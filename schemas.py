from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    balance: int | None = 0
    full_name: str | None = None
    disabled: bool | None = None

class Order(BaseModel):
    item_name: str
    type: str
    quantity: int

class UserInDB(User):
    hashed_password: str
