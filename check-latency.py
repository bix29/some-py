from elasticsearch import Elasticsearch
from elasticsearch import helpers
import datetime
import requests
import json


es = Elasticsearch('123.123.123.123:9201')


sres = helpers.scan(es,
                    index="webhook-*",
                    preserve_order=True,
                    query={"query": {"bool": {"must": [{"query_string": {"query": "_type:notify  AND notify_number:1 AND paid_time:{2018-04-23T04:00 TO * }",          "analyze_wildcard": True}},      {
                        "range": {"@timestamp": {"gte": 1524457200000,            "lte": 1524461100000,            "format": "epoch_millis"}}}],    "must_not": []}}},
                    scroll="300s")


dd = {}
for i in range(1, 60000):
    try:
        i += 1
        print i
        hit = sres.next()
        msg = hit["_source"]
        idx = hit["_index"]
        sendtime = datetime.datetime.strptime(msg['send_time'], '%Y-%m-%dT%H:%M:%S')
        paidtime = datetime.datetime.strptime(msg['paid_time'], '%Y-%m-%dT%H:%M:%S')
        delay = (sendtime - paidtime).seconds

        acct_id = msg['acct_id']
        evt_id = msg['object_id']

        if delay >= 60:
            if not acct_id in dd.keys():
                dd[acct_id] = []
            if not evt_id in dd[acct_id]:
                dd[acct_id].append(evt_id)
    except:
        break


url = "http://123.123.123.123:9201/pro-logger_arfu%2A/_search"

payload = "{\n  \"version\": true,\n  \"size\": 0,\n  \"query\": {\n    \"bool\": {\n      \"must\": [\n        {\n          \"query_string\": {\n            \"query\": \"%s AND log_request_method:(GET OR Get OR get)\",\n            \"analyze_wildcard\": true\n          }\n        },\n        {\n          \"range\": {\n            \"@timestamp\": {\n              \"gte\": 1524457200000,\n              \"lte\": 1524463200000,\n              \"format\": \"epoch_millis\"\n            }\n          }\n        }\n      ],\n      \"must_not\": []\n    }\n  }\n}"

for k, v in dd.items():
    payload_get = payload % k
    response = requests.request("POST", url, data=payload_get)
    hits = json.loads(response.text)['hits']['total']
    # print hits
    # print response
    print("%s %s %s" % (k, len(v), hits))
