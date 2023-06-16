from flask import Blueprint, request, jsonify
import requests
import json
import datetime
from config import yatoken

tsearch = Blueprint('tsearch', __name__)

tokenexpire = '2023-05-27T10:11:47.199365354Z'
yatoken = yatoken

# Переменная для хранения временного ключа
temporary_token = None


def auth(token):
    current_time = datetime.datetime.now()
    print("current: ", current_time)
    global tokenexpire, temporary_token
    tokentime = tokenexpire[:-4]  # Убираем последние 4 символа, чтобы удалить дополнительные десятичные знаки
    print("tokentime: ", tokentime)
    timeobj = datetime.datetime.strptime(tokentime, "%Y-%m-%dT%H:%M:%S.%f")
    print(timeobj)
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    payload = json.dumps({
            "yandexPassportOauthToken": token
        })
    response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, data=payload).json()
    tokenexpire = response['expiresAt']
    temporary_token = response["iamToken"]
    print("token is off, new token: ",  tokenexpire, temporary_token)

    return temporary_token


@tsearch.route('/search', methods=['POST'])
def search():
    text = request.json['text']
    print(text)
    data = yasearch(text)  # Ваш список словарей
    count = yacount(text)
    return jsonify({'data': data, 'count': count, 'statuses': list(set([item['status'] for item in data]))})


def yasearch(value):
    url = "https://api.tracker.yandex.net/v2/issues/_search?perPage=10000"
    global temporary_token
    payload = json.dumps({
        "query": value
    })
    temporary_token = auth(yatoken)
    headers = {
        'Authorization': f'Bearer {temporary_token}',
        'X-Org-ID': '167455',
        'Content-Type': 'application/json',
        'Cookie': 'uid=5/0AAGRuOwY2OQF0BMsqAg=='
    }
    print(f"headers = {headers}")
    response = requests.request("POST", url, headers=headers, data=payload).json()
    keys = [item["key"] for item in response]
    description = [item["summary"] for item in response]
    status = [item["status"]["display"] for item in response]
    count = len(keys)
    # data = [{"key": key, "summary": description} for key, description in zip(keys, description)]
    data = [{"key": f"<a href='https://tracker.yandex.ru/{key}' target='_blank'>{key}</a>", "summary": description, "status": status} for key, description, status in zip(keys, description, status)]
    print(count)

    return data


def yacount(value):
    url = "https://api.tracker.yandex.net/v2/issues/_count"
    payload = json.dumps({
        "query": value
    })
    temporary_token = auth(yatoken)
    headers = {
        'Authorization': f'Bearer {temporary_token}',
        'X-Org-ID': '167455',
        'Content-Type': 'application/json',
        'Cookie': 'uid=5/0AAGRuOwY2OQF0BMsqAg=='
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()

    return response
