from typing import Dict, List
from fastapi import FastAPI, WebSocket, Depends, BackgroundTasks

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

order_book_snapshot: Dict[str, List[Dict[str, float]]] = {
    "bid": [],
    "ask": []
}

order_book_snapshot: Dict[str, List[Dict[str, float]]] = {
    "bid": [],
    "ask": []
}

active_websockets: List[WebSocket] = {}

