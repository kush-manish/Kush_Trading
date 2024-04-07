
import json
import uuid
from decimal import Decimal
from typing import Dict, List

import httpx
from fastapi import APIRouter, Depends, HTTPException

from .kafka import push_message
from ..database import orders, trades
from ..dependencies import get_current_user
from ..models import TokenData, Order, OrderResponseLimited, Trade

router = APIRouter()

@router.get("/trades", dependencies=[Depends(get_current_user)], response_model=List[Trade])
async def fetch_all_order(current_user: TokenData = Depends(get_current_user)):
    return trades.values()

