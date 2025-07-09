from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from engine import MatchingEngine
from models import Order
import asyncio
import time

app = FastAPI()
engine = MatchingEngine()

@app.get("/")
def read_root():
    return {"message": "Welcome to the GoQuant Matching Engine API!"}

# Connected clients
market_data_clients = []
trade_stream_clients = []

@app.post("/order")
async def submit_order(order: Order):
    order.timestamp = time.time()  # Ensure timestamp is added
    result = engine.submit_order(order)
    await broadcast_market_data(order.symbol)
    await broadcast_trade_data(result.get("trades", []))
    return result

@app.websocket("/ws/market_data")
async def market_data_ws(websocket: WebSocket):
    await websocket.accept()
    market_data_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        market_data_clients.remove(websocket)

@app.websocket("/ws/trades")
async def trade_ws(websocket: WebSocket):
    await websocket.accept()
    trade_stream_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        trade_stream_clients.remove(websocket)

async def broadcast_market_data(symbol):
    book = engine.get_book(symbol)
    data = {
        "symbol": symbol,
        "timestamp": time.time(),
        "asks": [[price, sum(order.quantity for order in book.asks[price])] for price in sorted(book.asks)[:10]],
        "bids": [[price, sum(order.quantity for order in book.bids[price])] for price in sorted(book.bids, reverse=True)[:10]],
    }
    for client in market_data_clients:
        try:
            await client.send_json(data)
        except:
            market_data_clients.remove(client)

async def broadcast_trade_data(trades):
    for trade in trades:
        for client in trade_stream_clients:
            try:
                await client.send_json(trade.dict())
            except:
                trade_stream_clients.remove(client)
