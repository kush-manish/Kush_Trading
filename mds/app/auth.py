from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# This is a simple example. Replace it with your database or secure token logic.
fake_users_db = {
    "johndoe": {
        "username": "mk",
        "full_name": "Manish Kushwaha",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return False
    if not fake_hash_password(password) == user['hashed_password']:
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Your token validation logic here
    user = fake_users_db.get("johndoe")  # Simplified for the example
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user