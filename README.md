# CryptexMatch

A high-performance cryptocurrency matching engine built with FastAPI. It supports various order types, provides real-time data via WebSocket, and is optimized for low-latency execution.

---

## Features

* Supports Limit, Market, IOC, and FOK order types
* Price-time priority matching algorithm
* Real-time Best Bid and Offer (BBO) and trade updates via WebSocket
* In-memory order book using efficient data structures
* Fully tested using Pytest

---

## Project Structure

```
CryptexMatch/
│
├── main.py                # FastAPI server and route definitions
├── engine.py              # Core Matching Engine logic
├── order_book.py          # OrderBook class with bid/ask queues
├── models.py              # Pydantic models for Order and Trade
├── bbo.py                 # WebSocket route for BBO streaming
├── tests/
│   └── test_engine.py     # Unit tests for engine
└── README.md              # Project documentation
```

---

## System Architecture

```
[Client] 
   ↓ 
REST API (FastAPI) 
   ↓ 
MatchingEngine 
   ↓ 
OrderBook 
   ↓ 
Real-time Updates via WebSocket
```

---

## Data Structures

* `defaultdict(deque)`: Used for bids and asks, ordered by price level
* `list`: Used to store completed trades
* Orders matched using FIFO within each price level

---

## Matching Algorithm

1. Based on price-time priority
2. Iterates through the opposite side of the order book
3. Matches aggressively as per order type rules (LIMIT, MARKET, IOC, FOK)
4. Handles partial and full fills
5. Adds unmatched limit orders back to the book

---

## API Endpoints

### HTTP

* `POST /order`: Submit a new order (JSON)

  * Fields: `symbol`, `side`, `order_type`, `quantity`, `price`, `order_id`, `timestamp`

### WebSocket

* `/ws/market_data/{symbol}`: Streams Best Bid/Offer for a symbol
* `/ws/trades`: Streams live trade executions

---

## Running the Server

```bash
uvicorn main:app --reload
```

Open your browser or Postman at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Testing

```bash
pytest tests/
```

---

## Requirements

* Python 3.9+
* FastAPI
* Uvicorn
* Pytest

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---



