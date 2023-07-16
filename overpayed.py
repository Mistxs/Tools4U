import requests
import json
from config import headers

from flask import Blueprint, request, jsonify

overpay = Blueprint('overpayed', __name__)

@overpay.route('/findoverpayed', methods=['POST'])
def overpayed():
    dataset = request.json['dataset']
    print(dataset)
    data = getTransactions(dataset["salon_id"], dataset["start_date"], dataset["end_date"])
    return jsonify({'success': True, "dataset" : data})

def checkDocuments(salon, docid):
    data = []
    url = f"https://api.yclients.com/api/v1/company/{salon}/sale/{docid}"
    response = requests.request("GET", url, headers=headers).json()
    payments = response["data"]["state"]["payment_transactions"]
    for item in payments:
        if item["sale_item_id"] == None:
            print("ALAAARM")
            data.append({
                "transaction_id": item["id"],
                "document_id": item["document_id"],
                "account": item["account_id"],
                "amount": item["amount"]
            })
            return True


def getTransactions(salon, startdate, enddate):
    url = f"https://api.yclients.com/api/v1/transactions/{salon}"
    data = []
    payload = json.dumps({
        "start_date": startdate,
        "end_date": enddate,
        'count': 1000
    })

    response = requests.request("GET", url, headers=headers, data=payload).json()
    print(response)
    for item in response["data"]:
        if checkDocuments(salon,item["document_id"]):
            print(item["record_id"])
            data.append({
                "id": item["id"],
                "date": item["date"],
                "amount": item["amount"],
                "record_id": item["record_id"]
            })
    return data

    # print(response)





