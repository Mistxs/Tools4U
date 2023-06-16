from flask import Blueprint, request
import requests
import json
import datetime

current_time = datetime.datetime.utcnow()
current_time_format = datetime.datetime.utcnow().isoformat() + 'Z'
delta = datetime.timedelta(days=7)
second_time = (current_time - delta).isoformat() + 'Z'


ucookie = Blueprint('ucookie', __name__)


@ucookie.route('/ucookie', methods=['POST'])
def kibana():
    text = request.json['text']
    print(text)
    data = getcookie(text)
    return data


def getcookie(user):
    url = "https://logs.yclients.cloud/internal/search/es"
    payload = json.dumps({
        "params": {
            "ignoreThrottled": True,
            "preference": 1684927512836,
            "index": "yclients-erp-api-requests-*",
            "body": {
                "version": True,
                "size": 500,
                "sort": [
                    {
                        "@timestamp": {
                            "order": "desc",
                            "unmapped_type": "boolean"
                        }
                    }
                ],
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "3h",
                            "time_zone": "Europe/Moscow",
                            "min_doc_count": 1
                        }
                    }
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "match": {
                                                "data.context.session_id": user
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": second_time,
                                        "lte": current_time_format,
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                },
                "highlight": {
                    "pre_tags": [
                        "@kibana-highlighted-field@"
                    ],
                    "post_tags": [
                        "@/kibana-highlighted-field@"
                    ],
                    "fields": {
                        "*": {}
                    },
                    "fragment_size": 2147483647
                }
            },
            "rest_total_hits_as_int": True,
            "ignore_unavailable": True,
            "ignore_throttled": True
        },
        "serverStrategy": "es"
    })
    headers = {
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'Content-Type': 'application/json',
        'kbn-version': '7.8.0',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'host': 'logs.yclients.cloud'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    # print(response)
    key = find_value(response, "session_id")

    # print(response["rawResponse"]["hits"]["hits"][0]["_source"]["data"]["context"]["session_id"])
    return key


def find_value(json_obj, target_key):   
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key == target_key:
                return value
            elif isinstance(value, (dict, list)):
                result = find_value(value, target_key)
                if result is not None:
                    return result
    elif isinstance(json_obj, list):
        for item in json_obj:
            result = find_value(item, target_key)
            if result is not None:
                return result

    return None
