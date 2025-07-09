from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

class Order(BaseModel):
    order_id: str = str(uuid4())
    symbol: str
    order_type: str  # "market", "limit", "ioc", "fok"
    side: str  # "buy", "sell"
    quantity: float
    price: Optional[float] = None
    timestamp: float

class TradeExecution(BaseModel):
    timestamp: float
    symbol: str
    trade_id: str
    price: float
    quantity: float
    aggressor_side: str  # "buy" or "sell"
    maker_order_id: str
    taker_order_id: str
