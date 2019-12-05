import time

from elasticsearch_dsl import connections, MultiSearch

from filters.flat_price_filters import AskPriceFilter, BidPriceFilter

connections.create_connection()


def run_multiple_filters():
    while True:
        index = "book"
        ms = MultiSearch(index=index)
        ask_price_filter = AskPriceFilter(index)
        search_ask = ask_price_filter.main_query(
            gt_price=50, lt_price=52, from_range=10, to_range=20
        )
        ms = ms.add(search_ask)
        bid_price_filter = BidPriceFilter(index)
        search_bid = bid_price_filter.main_query(gt_price=50, lt_price=51, to_range=15)
        ms = ms.add(search_bid)

        responses = ms.execute()  # returns a list of Response objects
        for resp in responses:
            print(len(resp))
            print(resp.hits.total.value)

        ask_price_filter.show_result(from_range=0, to_range=5)
        bid_price_filter.show_result(from_range=0, to_range=5)

        time.sleep(5)


if __name__ == "__main__":
    run_multiple_filters()
