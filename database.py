
from passlib.context import CryptContext

from schemas import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


fake_users_db = {
    "mk": {
        "username": "mk",
        "full_name": "Manish Kushwaha",
        "balance":100000,
        "email": "mkk9313@email.com",
        "hashed_password": "$2b$12$Y.LHFu/99GIGmlpsuaJJlenGAtc/KTMnsMDiU/gBPaUAcS0ADuoMq",
        "disabled": False,
    },
    "ms": {
        "username": "ms",
        "full_name": "Manish Sharma",
        "balance":50000,
        "email": "mkk9313@email.com",
        "hashed_password": "$2b$12$Y.LHFu/99GIGmlpsuaJJlenGAtc/KTMnsMDiU/gBPaUAcS0ADuoMq",
        "disabled": False,
    },
    "mv": {
        "username": "mv",
        "full_name": "Manish Verma",
        "balance":25000,
        "email": "mkk9313@email.com",
        "hashed_password": "$2b$12$Y.LHFu/99GIGmlpsuaJJlenGAtc/KTMnsMDiU/gBPaUAcS0ADuoMq",
        "disabled": False,
    }
}
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
