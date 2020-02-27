import typing
from abc import ABC, abstractmethod

from elasticsearch_dsl import Search, connections
from elasticsearch_dsl.response import Response

connections.create_connection()


class BaseFilter(ABC):
    def __init__(self, index: str) -> None:
        self.search = Search(index=index)

    @abstractmethod
    def main_query(self, *args, **kwargs):
        pass

    @abstractmethod
    def show_result(
        self,
        response: Response,
        from_range: typing.Optional[int] = None,
        to_range: typing.Optional[int] = None,
    ) -> None:
        pass


