from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch.client import CatClient
from elasticsearch.helpers import bulk


def first_example(es: Elasticsearch):
    data = (
        '{ "index" : { "_index" : "test", "_id" : "1" } }\n{ "field1" : "value1" }\n'  # ~= PUT
        '{ "delete" : { "_index" : "test", "_id" : "2" } }\n'
        '{ "create" : { "_index" : "test", "_id" : "3" } }\n{ "field1" : "value3" }\n'  # ~= POST
        '{ "update" : {"_id" : "1", "_index" : "test"} }\n{ "doc" : {"field2" : "value2"} }'  # ~= PATCH
    )
    es.bulk(data)
    es.count(index="test")
    es.delete(index="test", id="1")

    assert es.exists(index="test", id=0) == False
    assert es.exists(index="test", id=3) == True

    update_body = '{"script": {"source": "ctx._source.field1 = params.val", "lang": "painless", "params": {"val": "another"}}}'
    es.update(index="test", id="3", body=update_body)

    es.indices.delete("test")
    indices = es.indices.get("*")  # retrieve all the indices
    assert "test" not in indices.keys()


def bank_example(es: Elasticsearch):
    with open("accounts.json", "r") as f:
        bank_data = f.read()

    es.bulk(body=bank_data, index="bank")

    es.search(
        index="bank",
        body='{"query": {"match": {"firstname": "Fulton"}}}',
        filter_path="hits.hits._source.firstname, hits.hits._source.lastname, hits.hits._id",
    )

    cat = CatClient(client=es)
    assert cat.count(index=["bank"], format="json")[0]["count"] == "1000"


def many_indices_example(es: Elasticsearch):
    # It's possible to search without specifying the index: ES will search in all the indices.
    try:
        es.indices.delete(index="test")
        es.indices.delete(index="other")
    except NotFoundError:
        pass

    # assert not es.indices.exists("test") or es.count(index="test")["count"] == 0
    # assert not es.indices.exists("other") or es.count(index="other")["count"] == 0

    data = (
        '{ "index" : { } }\n{ "field1" : "value1" }\n'
        '{ "index" : { } }\n{ "field1" : "value2" }\n'
        '{ "index" : { } }\n{ "field1" : "value3" }\n'
    )
    other_data = (
        '{ "index" : { "_index" : "other", "_id" : "42" } }\n{ "field1" : "value1" }\n'
        '{ "index" : { "_index" : "other", "_id" : "43" } }\n{ "field1" : "value2" }\n'
    )

    es.bulk(body=data, index="test", refresh="wait_for")
    es.bulk(body=other_data, refresh="wait_for")

    test_count = es.count(index="test")["count"]
    assert test_count == 3
    other_count = es.count(index="other")["count"]
    print(other_count, other_count == 2)
    assert other_count == 2

    response = es.search(body='{"query": {"match": {"field1": "value1"}}}')
    assert response["hits"]["total"]["value"] == 2

    es.indices.delete(index="test")
    es.indices.delete(index="other")


def bulk_helper_example(es):
    try:
        es.indices.delete(index="other")
    except NotFoundError:
        pass

    bulk_data = [
        {
            "_index": "other",
            "_type": "_doc",
            "_id": "42",
            "_score": 1.0,
            "_source": {"field1": "value1"},
        },
        {
            "_index": "other",
            "_type": "_doc",
            "_id": "43",
            "_score": 1.0,
            "_source": {"field1": "value2"},
        },
    ]

    bulk(es, bulk_data, refresh="true")
    other_count = es.count(index="other")["count"]
    assert other_count == 2


if __name__ == "__main__":
    es = Elasticsearch()
    # first_example(es)
    # bank_example(es)
    # many_indices_example(es)
    bulk_helper_example(es)
