import asyncio
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from engine import MatchingEngine

router = APIRouter()
engine = MatchingEngine()

@router.websocket("/ws/market_data/{symbol}")
async def market_data(websocket: WebSocket, symbol: str):
    await websocket.accept()
    try:
        while True:
            book = engine.get_book(symbol)
            bid, ask = book.get_bbo()  # Ensure this function exists in OrderBook
            await websocket.send_json({
                "symbol": symbol,
                "bbo": {
                    "best_bid": bid,
                    "best_ask": ask
                }
            })
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print(f"Client disconnected from {symbol} BBO stream")
