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
