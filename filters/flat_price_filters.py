import typing
from abc import abstractmethod, ABC

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Range


class BaseFilter(ABC):
    def __init__(self, index: str) -> None:
        self.search = Search(index=index)

    @abstractmethod
    def main_query(self, *args, **kwargs) -> Search:
        pass

    @abstractmethod
    def show_result(
        self,
        from_range: typing.Optional[int] = None,
        to_range: typing.Optional[int] = None,
    ) -> None:
        """Intended for debugging; likely to be removed soon!"""
        pass


class AskPriceFilter(BaseFilter):
    def main_query(
        self,
        gt_price: float = 0.0,
        lt_price: float = 10 ** 6,
        from_range: int = 0,
        to_range: int = 10,
        *args,
        **kwargs,
    ):
        range_q = Range(askPrice={"gt": gt_price, "lt": lt_price})
        s = self.search.query(range_q)
        s = s.update_from_dict({"collapse": {"field": "symbol.keyword"}})
        s = s.sort("-timeStamp")[from_range:to_range]

        self.search = s

        return s

    def show_result(
        self,
        from_range: typing.Optional[int] = None,
        to_range: typing.Optional[int] = None,
    ) -> None:
        res = self.search.execute()

        res_range = slice(from_range, to_range)
        for hit in res[res_range]:
            date = f"{hit.timeStamp[:10]} {hit.timeStamp[11:19]}"
            print(f"Asset: {hit.symbol}, ASK PRICE: {hit.askPrice}, DATE: {date}")


class BidPriceFilter(BaseFilter):
    def main_query(
        self,
        gt_price: float = 0.0,
        lt_price: float = 10 ** 6,
        from_range: int = 0,
        to_range: int = 10,
        *args,
        **kwargs,
    ):
        range_q = Range(bidPrice={"gt": gt_price, "lt": lt_price})
        s = self.search.query(range_q)
        s = s.update_from_dict({"collapse": {"field": "symbol.keyword"}})
        s = s.sort("-timeStamp")[from_range:to_range]

        self.search = s

        return s

    def show_result(
        self,
        from_range: typing.Optional[int] = None,
        to_range: typing.Optional[int] = None,
    ) -> None:
        res = self.search.execute()

        res_range = slice(from_range, to_range)
        for hit in res[res_range]:
            date = f"{hit.timeStamp[:10]} {hit.timeStamp[11:19]}"
            print(f"Asset: {hit.symbol}, BID PRICE: {hit.bidPrice}, DATE: {date}")