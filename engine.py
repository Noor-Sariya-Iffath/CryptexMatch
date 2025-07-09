import time
import uuid
from order_book import OrderBook
from models import TradeExecution

class MatchingEngine:
    def __init__(self):
        self.books = {}  # symbol: OrderBook
        self.trades = []  # List of all trades

    def get_book(self, symbol):
        if symbol not in self.books:
            self.books[symbol] = OrderBook()
        return self.books[symbol]

    def submit_order(self, order):
        book = self.get_book(order.symbol)
        trades = []

        # Determine opposite book
        if order.side == "buy":
            opposite_book = book.asks
            match_prices = sorted(opposite_book)
            price_check = lambda p: True if order.order_type == "market" else p <= order.price
        else:
            opposite_book = book.bids
            match_prices = sorted(opposite_book, reverse=True)
            price_check = lambda p: True if order.order_type == "market" else p >= order.price

        quantity_to_fill = order.quantity

        for price in match_prices:
            if not price_check(price):
                break

            resting_orders = opposite_book[price]

            while resting_orders and quantity_to_fill > 0:
                resting_order = resting_orders[0]
                trade_qty = min(quantity_to_fill, resting_order.quantity)

                trade = TradeExecution(
                    timestamp=time.time(),
                    symbol=order.symbol,
                    trade_id=str(uuid.uuid4()),
                    price=price,
                    quantity=trade_qty,
                    aggressor_side=order.side,
                    maker_order_id=resting_order.order_id,
                    taker_order_id=order.order_id,
                )

                trades.append(trade)
                self.trades.append(trade)

                resting_order.quantity -= trade_qty
                quantity_to_fill -= trade_qty

                if resting_order.quantity == 0:
                    resting_orders.popleft()

            if not resting_orders:
                del opposite_book[price]

            if quantity_to_fill <= 0:
                break

        # Handle leftovers
        if quantity_to_fill > 0:
            if order.order_type == "limit":
                order.quantity = quantity_to_fill
                resting_book = book.bids if order.side == "buy" else book.asks
                resting_book[order.price].append(order)
                return {
                    "status": "partially_filled" if trades else "rested",
                    "order_id": order.order_id,
                    "trades": trades
                }

            elif order.order_type == "ioc":
                return {
                    "status": "partially_filled" if trades else "canceled",
                    "canceled_qty": quantity_to_fill,
                    "trades": trades
                }

            elif order.order_type == "fok":
                return {
                    "status": "rejected",
                    "reason": "FOK not fully fillable"
                }

        return {
            "status": "filled" if trades else "no_match",
            "order_id": order.order_id,
            "trades": trades
        }
