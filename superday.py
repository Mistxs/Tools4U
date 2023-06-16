from flask import jsonify, request, Blueprint
import requests
import json

from config import headers


superday = Blueprint('superday', __name__)


salon = 543449


@superday.route('/superday', methods=['POST'])
def parse():
    date = request.json['date']
    global salon
    salon = request.json['salon']
    print(salon, date)
    return jsonify(getrecords(date))


def getsales(docid):
    url = f"https://api.yclients.com/api/v1/company/{salon}/sale/{docid}"
    payload = {}
    bpsatatus = {
        1: "Чек не распечатан",
        2: "Печатается чек продажи",
        3: "Напечатан чек продажи",
        4: "Печатается чек возврата",
        5: "Напечатан чек возврата"
    }
    costtotal = 0
    payments = 0
    loyalty = 0
    more = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    state = response["data"]["state"]
    items = state["items"]
    loyalty_transactions = state["loyalty_transactions"]
    payment_transactions = state["payment_transactions"]
    for item in items:
        costtotal += item["cost_to_pay_total"]
    for transaction in loyalty_transactions:
        if transaction["type_id"] in [1, 3, 8, 9, 10, 11]:
            loyalty += transaction["amount"]
    for transaction in payment_transactions:
        payments += transaction["amount"]
    payment_status = "Ошибок в оплате нет" if loyalty + payments == costtotal else "Есть ошибка в оплате"
    bills = None
    transactions = response["data"]["kkm_state"]["transactions"]
    if transactions:
        bills = transactions[0]["document"]["bill_print_status"]
    bilstat = bpsatatus.get(bills, "Чек не печатался")
    more = {
        "costtotal": costtotal,
        "loyalty": loyalty,
        "payments": payments,
        "payment_status": payment_status,
        "bill_status": bilstat
    }
    return more, bilstat


def getrecords(date):
    attendance = {
        -1: "Клиент не пришел",
        0: "Ожидание клиента",
        1: "Клиент пришел",
        2: "Клиент подтвердил"
    }
    paid = {
        0: "Не оплачена",
        1: "Оплачена",
        2: "Переплата"
    }
    bills = {
        "False": "Не распечатан",
        "True": "Распечатан"
    }
    output = []
    url = f"https://api.yclients.com/api/v1/records/{salon}"
    payload = json.dumps({
        "start_date": date,
        "end_date": date
    })
    response = requests.request("GET", url, headers=headers, data=payload).json()
    for item in response["data"]:
        services = []
        clients = {}
        documents = []
        for service in item["services"]:
            services.append({
                "id": service["id"],
                "title": service["title"]
            })

        if item["client"] is not None:
            clients = {
                "id": item["client"].get("id", ""),
                "name": item["client"].get("name", ""),
                "phone": item["client"].get("phone", "")
            }
        for document in item["documents"]:
            documents.append({
                "id": document["id"],
                "number": document["number"],
                "type": document["type_id"],
                "title": document["type_title"]
            })
        bill = str(item["is_sale_bill_printed"])
        shortdate = item["date"].split(" ")[0]
        salesinfo, bs = getsales(item["documents"][0]["id"])
        output.append({
            "staff": item["staff_id"],
            "staff_name": item["staff"]["name"],
            "services": services,
            "client": clients,
            "date": f'<a href="https://yclients.com/timetable/{salon}#main_date={shortdate}&open_modal_by_record_id={item["id"]}" target=_blank>{item["date"]}</a>',
            "attendance": attendance.get(item["attendance"]),
            "paid" : paid.get(item["paid_full"]),
            "bills": bs,
            "more" : [{
            "record_id" : item["id"],
            "visit_id": item["visit_id"],
            "documents": documents,
            "salesinfo": salesinfo
            }]

        })
    return output
