from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Text, Double, Long, Date, Keyword, connections

connections.create_connection()
es = Elasticsearch()


class GeneralDoc(Document):
    symbol = Keyword()  # Text(fields={"keyword": Keyword()})
    company_name = Text()

    high_52_week = Double()
    low_52_week = Double()
    close_price = Double()
    avg_volume_30_days = Long()

    timestamp = Date()

    def save(self, **kwargs):
        self.timestamp = datetime.now()
        return super().save(**kwargs)

    class Index:
        name = "general"


class TaSDoc(Document):
    symbol = Keyword()
    last_price = Double()
    update_time = Date()
    last_exch = Keyword()
    last_size = Long()

    timestamp = Date()

    def save(self, **kwargs):
        self.timestamp = datetime.now()
        return super().save(**kwargs)

    class Index:
        name = "tas"


class BookDoc(Document):
    symbol = Keyword()
    bid_size = Long()
    ask_size = Long()
    bid_price = Double()
    ask_price = Double()
    open_price = Double()
    update_time = Date()

    timestamp = Date()

    def save(self, **kwargs):
        self.timestamp = datetime.now()
        return super().save(**kwargs)

    class Index:
        name = "book"


if __name__ == "__main__":
    GeneralDoc.init()
    TaSDoc.init()
    BookDoc.init()
