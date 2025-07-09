from collections import deque, defaultdict

class OrderBook:
    def __init__(self):
        self.bids = defaultdict(deque)  # price: deque of buy orders
        self.asks = defaultdict(deque)  # price: deque of sell orders

    def add_order(self, order):
        book = self.bids if order.side == "buy" else self.asks
        book[order.price].append(order)

    def get_bbo(self):
        best_bid = max(self.bids.keys()) if self.bids else None
        best_ask = min(self.asks.keys()) if self.asks else None
        return best_bid, best_ask
