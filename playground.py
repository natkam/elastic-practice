from elasticsearch import Elasticsearch
from elasticsearch.client import CatClient


es = Elasticsearch()

data = (
    '{ "index" : { "_index" : "test", "_id" : "1" } }\n{ "field1" : "value1" }\n'
    '{ "delete" : { "_index" : "test", "_id" : "2" } }\n'
    '{ "create" : { "_index" : "test", "_id" : "3" } }\n{ "field1" : "value3" }\n'
    '{ "update" : {"_id" : "1", "_index" : "test"} }\n{ "doc" : {"field2" : "value2"} }'
)

es.bulk(data)
es.count(index="test")
es.delete(index="test", id="1")

assert es.exists(index="test", id=0) == False
assert es.exists(index="test", id=3) == True

update_body = '{"script": {"source":"ctx._source.field1 = params.val", "lang":"painless", "params": {"val": "another"}}}'
es.update(index="test", id="3", body=update_body)

es.indices.delete("test")
indices = es.indices.get("*")  # retrieve all the indices
assert "test" not in indices.keys()


with open("accounts.json", "r") as f:
    bank_data = f.read()

es.bulk(body=bank_data, index="bank")

es.search(
    index="bank",
    body='{"query": {"match": {"firstname": "Fulton"}}}',
    filter_path="hits.hits._source.firstname, hits.hits._source.lastname, hits.hits._id",
)

cat = CatClient(client=es)
cat.count(index=["bank"], format="json")
