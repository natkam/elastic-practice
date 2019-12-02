import json
import random
import typing
from string import ascii_uppercase


STOCK_EXCHANGES = ["ARCA", "NYSE", "EDGX", "EDGA", "BATS"]


def generate_ticker() -> str:
    return "".join(random.sample(ascii_uppercase, 4))


def generate_bid_prices(suggested_price: float = 10.00) -> typing.List[float]:
    return [
        round(random.gauss(mu=suggested_price, sigma=suggested_price / 100), ndigits=2)
        for _ in range(3)
    ]


def generate_ask_prices(bid_prices: typing.List[float]) -> typing.List[float]:
    return [
        round(bid + random.choice([0.05, 0.1, 0.15]), ndigits=2) for bid in bid_prices
    ]


def generate_quota() -> str:
    return str(random.randint(1, 20) * 100)


def generate_order_book(ticker: str) -> typing.Dict:
    bid_prices = generate_bid_prices()
    bid = {
        str(bid): {exchange: generate_quota() for exchange in STOCK_EXCHANGES}
        for bid in bid_prices
    }
    ask_prices = generate_ask_prices(bid_prices)
    ask = {
        str(ask): {exchange: generate_quota() for exchange in STOCK_EXCHANGES}
        for ask in ask_prices
    }
    order_book = {"ticker": ticker, "order_book": {"bid": bid, "ask": ask}}
    return order_book


if __name__ == "__main__":
    with open("order_book.json", "w") as f:
        for index in range(100):
            index_info = {"index": {"_id": index}}
            f.write(json.dumps(index_info) + "\n")
            f.write(json.dumps(generate_order_book(generate_ticker())) + "\n")
