import typing
from datetime import datetime

from elasticsearch_dsl import A, Q, Search
from elasticsearch_dsl.aggs import ExtendedStats, Nested, Agg
from elasticsearch_dsl.query import MatchAll

from filters.base_filter import BaseFilter


class AskPriceFilter(BaseFilter):
    def main_query(
        self, gt_price: float = 5.0, lt_price: float = 50.0, *args, **kwargs
    ):

        range_query = Q("range", asset__ask__price={"gt": gt_price, "lt": lt_price})
        q = self.search.query("nested", path="asset.ask", query=range_query)
        q = q.sort("-timestamp")
        response = q.execute()

        return response

    def show_result(
        self,
        response: Search,
        from_range: typing.Optional[int] = None,
        to_range: typing.Optional[int] = None,
    ) -> None:
        res_range = slice(from_range, to_range)
        for hit in response[res_range]:
            max_price = max(x.price for x in hit.asset[0].ask)
            # asset list only contains one element
            # TODO: change the mapping of `asset` from `Nested` to `Object` (?)
            date = datetime.strptime(hit.timestamp, "%Y-%m-%dT%H:%M:%S.%f").strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            print(f"Asset: {hit.asset[0].ticker}, ID: {hit.meta.id}")
            print(f"MAX ASK PRICE: {max_price}, DATE: {date}")


class BidPriceFilter(BaseFilter):
    def main_query(
        self, gt_price: float = 5.0, lt_price: float = 50.0, *args, **kwargs
    ):
        range_query = Q("range", asset__bid__price={"gt": gt_price, "lt": lt_price})
        q = self.search.query("nested", path="asset.bid", query=range_query)
        q = q.sort("-timestamp")
        response = q.execute()

        return response

    def show_result(
        self,
        response: Search,
        from_range: typing.Optional[int] = None,
        to_range: typing.Optional[int] = None,
    ) -> None:
        res_range = slice(from_range, to_range)
        for hit in response[res_range]:
            min_price = min(bid.price for bid in hit.asset[0].bid)
            date = datetime.strptime(hit.timestamp, "%Y-%m-%dT%H:%M:%S.%f").strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            print(f"Asset: {hit.asset[0].ticker}, ID: {hit.meta.id}")
            print(f"MIN BID PRICE: {min_price}, DATE: {date}")


class AskPriceStdDeviationFilter(BaseFilter):
    def main_query(self, start_time=None, *args, **kwargs):
        # TODO: make sure the start_time format matches "2019-11-28T13:02:05.912360"
        #  (is it "%Y-%m-%dT%H:%M:%S.%f"?)
        nested = Q("nested", path="asset.ask", query=MatchAll())
        q = self.search.query(nested)
        # TODO: set `size=0`! (no need to return all the records)

        if start_time is not None:
            # timestamp_filter = Q("bool", filter=[Q("range", timestamp={"gte": start_time})])
            q = q.filter("range", timestamp={"gte": start_time})

        nested_stat = Nested(path="asset.ask")
        ask_std = ExtendedStats(field="asset.ask.price")
        # ask_std = A("extended_stats", field="asset.ask.price")


        print(q.to_dict())
        response = q.execute()

        return response

    def show_result(
        self,
        response: Search,
        from_range: typing.Optional[int] = None,
        to_range: typing.Optional[int] = None,
    ) -> None:
        # res_range = slice(from_range, to_range)
        std_dev = response.aggs.ask_price.stats.str_deviation
        print(std_dev)
