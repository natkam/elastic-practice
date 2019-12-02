from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections, Search

connections.create_connection(hosts="localhost", timeout=20)


def prepare_data():
    es = Elasticsearch()
    with open("order_book.json", "r") as f:
        data = f.read()

    es.bulk(body=data, index="order")
    assert len(Search(index="order").query("match_all").execute()) == 10
    print("Loaded the order book data.")


def search_example():
    s = Search(index="order")
    sq_1 = s.query("match", ticker="XGNO")
    response_1 = sq_1.execute()

    print(response_1)

    for i, hit in enumerate(response_1):
        print(f"{i}: {hit.ticker}, {hit.order_book.bid['10.05']}")

    sq2 = Search(index="order").query("match_all")
    response_2 = sq2.execute()

    print(response_2)
    print(len(response_2.hits))

    for hit in response_2:
        print(hit)


def many_indices_example(es: Elasticsearch):
    # It's possible to search without specifying the index: ES will search in all the indices.
    pass


if __name__ == "__main__":
    es = Elasticsearch()
    prepare_data()
    # many_indices_example(es)
