from elasticsearch import Elasticsearch


es = Elasticsearch()

if es.indices.exists("order"):
    es.indices.delete("order")

with open("order_book.json", "r") as f:
    order_data = f.read()

# print(es.bulk(body=order_data, index="order", filter_path=["took", "errors"]))
print(es.bulk(body=order_data, index="order"))
# only 84 out of 100 docs are loaded!
# "Limit of total fields [1000] in index [order] has been exceeded" :(

print(es.count(index="order"))