import random
import time
import typing
from datetime import datetime, timedelta

from doc_mapping import GeneralDoc, TaSDoc, BookDoc

ECN_PROVIDERS = ["ARCA", "NYSE", "EDGX", "EDGA", "BATS"]
ASSET_SYMBOLS = ["AAPL", "FB", "AMZN", "ROKU", "MSFT"]
COMPANY_NAMES = ["Apple", "Facebook", "Amazon", "Roku", "Microsoft Corporation"]
ASSETS = {asset: name for asset, name in zip(ASSET_SYMBOLS, COMPANY_NAMES)}


def fake_general_doc(previous_price: typing.Optional[float] = None) -> GeneralDoc:
    symbol = random.choice(ASSET_SYMBOLS)
    company_name = ASSETS[symbol]

    _base_price = previous_price or 10.0
    close_price = round(
        random.gauss(mu=_base_price, sigma=_base_price / 100), ndigits=2
    )
    high_52_week = close_price + 2
    low_52_week = close_price - 2
    avg_volume_30_days = random.randint(10, 200) * 10

    # timestamp = datetime.now()

    general_data = {
        "symbol": symbol,
        "company_name": company_name,
        "high_52_week": high_52_week,
        "low_52_week": low_52_week,
        "close_price": close_price,
        "avg_volume_30_days": avg_volume_30_days,
        # "timestamp": timestamp,
    }

    return GeneralDoc(**general_data)


def fake_TaS_doc(previous_price: typing.Optional[float] = None) -> TaSDoc:
    symbol = random.choice(ASSET_SYMBOLS)
    last_exch = random.choice(ECN_PROVIDERS)

    _base_price = previous_price or 10.0
    last_price = round(random.gauss(mu=_base_price, sigma=_base_price / 100), ndigits=2)
    last_size = random.randint(1, 20) * 100
    update_time = datetime.now() - timedelta(seconds=random.randint(1, 5))

    # timestamp = datetime.now()

    tas_data = {
        "symbol": symbol,
        "last_exch": last_exch,
        "last_price": last_price,
        "last_size": last_size,
        "update_time": update_time,
        # "timestamp": timestamp,
    }

    return TaSDoc(**tas_data)


def fake_book_doc(previous_price: typing.Optional[float] = None) -> BookDoc:
    symbol = random.choice(ASSET_SYMBOLS)
    bid_size = random.randint(1, 20) * 100
    ask_size = bid_size + random.choice(range(-100, 100, 10))

    _base_price = previous_price or 10.0
    bid_price = round(random.gauss(mu=_base_price, sigma=_base_price / 100), ndigits=2)
    ask_price = round(bid_price + random.choice([0.05, 0.1, 0.15]), ndigits=2)
    open_price = _base_price
    update_time = datetime.now() - timedelta(seconds=random.randint(1, 5))

    # timestamp = datetime.now()

    book_data = {
        "symbol": symbol,
        "bid_size": bid_size,
        "ask_size": ask_size,
        "bid_price": bid_price,
        "ask_price": ask_price,
        "open_price": open_price,
        "update_time": update_time,
        # "timestamp": timestamp,
    }

    return BookDoc(**book_data)


if __name__ == "__main__":
    while True:
        GeneralDoc.init()
        general = fake_general_doc()
        general.save()
        print(f"General doc has been saved: {general}")

        TaSDoc.init()
        tas = fake_TaS_doc()
        tas.save()
        print(f"TaS doc has been saved: {tas}")

        BookDoc.init()
        book = fake_book_doc()
        book.save()
        print(f"Book doc has been saved: {book}")

        time.sleep(2)
