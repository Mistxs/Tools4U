from flask import Blueprint, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import json

fsr = Blueprint('fsr', __name__)

baseurl = "https://yclients.com"

# product
auth_cookie = "__ddg1_=exsBazo8eGkna9M9Uomc; _cmg_csst1lPaz=1678712167; _comagic_id1lPaz=6941324878.10216608865.1678712167; _fbp=fb.1.1681128751602.1057597157; _ga=GA1.2.1928824817.1674055633; _ga_6EVFCY524B=GS1.1.1681134483.7.0.1681134486.0.0.0; _ga_P2LM7D8KSM=GS1.1.1683879274.17.0.1683879286.48.0.0; _gcl_au=1.1.919775470.1681900667; _ym_d=1674055633; _ym_uid=1674055633835203884; adrcid=AWjpZrOjq6FN88BP4tS2H8A; analytics-udid=G4EOvZYRcXAD9bObLSz4H6iBqHxdJXqcSVkhmRqN; app_service_level=0; app_service_level_ttl=1684482773; auth=u-11946640-e3689818c34c48aa83db4; tmr_lvid=35025bf4d92d6dc445d8f77c6cd09cfd; tmr_lvidTS=1674055632559; x-feature-waiting-room=0; yc_user_id=11946640; app_service_group=9; _ym_isad=2; tracking-index=1457; ycl_language_id=1; yc_company_id=543449; _cfuvid=m.LlGW_RF.J8iiSU_phnYHK7ACO55s2lVQY8Avwfa7s-1684430721275-0-604800000; __cfwaitingroom=ChhQb1hoNmcxOXZ5RFV4NU1UL2tYV3N3PT0SrAJpL1FLTldOTWE1TnZnSnBGcDU2YTFrNlFaVjdmMDBrMjRvQm4yVzVFZVE5bndnM3hHU3IybjNEOTZuMFE2Zml2Nll2TmU2cnNhdno4TGxsK1BVSzk2NGNqdEFCai94dkJqZkZkK2U0R1BMNEhCcFdmT2tGSkx2czFoRnVMM2dPd0l5blFiWE5xYWNpL2VUK0k0NXUzekI2NHdWdlJhbWNtQ2o2VHZYbWVYbzJuNmRxM0FreStVSE5PQm52S1dKT3FaQjljYmRaVnIyZ0d1S3p2WEFiR015eFk1WldaQms4YkNOQzhPNVVveTA5ZG1ybERacXg5eEQ3R3NHUVRmRlptaFhqTWxaNWxZWnJVeTlSSHUvTW45cU9IQ1Z1VlVNMTNOYUhJMFdVN0tLQT0%3D; __cf_bm=89PvUcd9QeXqeECWS9nZGP9IURUhVcEdDYYHdPH6G3Q-1684430722-0-ARkDth9CncmZbT+jMmYmKpLV6E1CX0d4YzFVFYqoEKtEMI02MJLldFqKlKGkThOQgBtWA+QBXyuaGfOCPsprQhW3k1XN8XoukWPNEF6QxXT89kmm7sk9JEKT22zo9u3Z6fHGInlOIKtuCymZD6+zcCc="
headers = {
    'Content-Type': 'application/json',
    'Authorization': '93z5f8fmhcydaa2pj4ca, e69793634796c00b57cb4bfd34f361d8',
    'Accept': 'application/vnd.yclients.v2+json'
}

def getdata(url):

    # Отправляем GET-запрос с передачей Cookie
    global document_id
    response = requests.get(url, cookies={"Cookie": auth_cookie})
    kkm_response = {}
    # Проверяем код состояния ответа (200 означает успешный запрос)
    if response.status_code == 200:
        html_content = response.text
        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(html_content, "html.parser")
        # Находим все элементы с классом "ibox-content"
        ibox_contents = soup.find_all("div", class_="ibox-content")
        # Находим все элементы <td> внутри таблицы
        td_elements = soup.find("table", class_="table").find_all("td")
        # Получаем содержимое нужного элемента <td> по индексу
        document_id = td_elements[1].get_text(strip=True)

        # Находим элемент <li> с классом "calendar-toggle"
        li_element = soup.find("li", class_="calendar-toggle")
        # Находим элемент <a> внутри элемента <li>
        a_element = li_element.find("a")
        # Получаем значение атрибута href
        href_value = a_element.get("href")
        # Извлекаем значение после префикса "/timetable/"
        salon_id = href_value.split("/timetable/")[1]
        # Вывод значения переменной value

        # Проверяем, есть ли второй блок
        if len(ibox_contents) >= 2:
            # Получаем второй блок с классом "ibox-content"
            second_block = ibox_contents[1]

            # Извлекаем текст из второго блока
            second_content = second_block.get_text(strip=True)
            kkm_response = json.loads(second_content)




        else:
            print("Не удалось найти второй блок с классом 'ibox-content'.")
    else:
        print("Ошибка при выполнении запроса:", response.status_code)

    kkm_id = url.split("/")[-2]
    return kkm_id,kkm_response,document_id,salon_id

@fsr.route('/check_document', methods=['POST'])
def check_document():
    kkm_link = request.json['kkm_link']
    if not is_valid_link(kkm_link):
        return 'CHECKDOCUMENT. Некорректная ссылка, проверьте написание'
        # Выполнение функции getdocumentstatus(kkm_link)
    result = getdocumentstatus(kkm_link)
    return result

@fsr.route('/kkmresponse', methods=['POST'])
def kkmresponse():
    kkm_link = request.json['kkm_link']
    if not is_valid_link(kkm_link):
        return 'kkmresponse. Некорректная ссылка, проверьте написание'
        # Выполнение функции getdocumentstatus(kkm_link)
    kkm, resp, document, salon_id = getdata(kkm_link)
    return resp


@fsr.route('/get_payload', methods=['POST'])
def get_payload():
    kkm_link = request.json['kkm_link']
    print(kkm_link)
    if not is_valid_link(kkm_link):
        return jsonify({'error': 'GETPAYLOAD. Некорректная ссылка, проверьте написание'})
    kkm, resp, document, salon_id = getdata(kkm_link)
    payload, warning = generate_payload(kkm,resp)
    text = "OK"
    # if warning == 1:
    #     text = "Внимание! В ответе от ккмсервера нет данных из ОФД. Отправляете запрос на свой страх и риск!"
    #     return jsonify([payload, text])  # Возвращаем список с payload и text

    return payload  # Возвращаем список с payload


@fsr.route('/run_force', methods=['POST'])
def run_force():
    kkm_link = request.json['kkm_link']
    if not is_valid_link(kkm_link):
        return jsonify({'error': 'GETPAYLOAD. Некорректная ссылка, проверьте написание'})
    # Остальная логика выполнения force и получения результата
    kkm, resp, document, salon_id = getdata(kkm_link)
    result = execute_force(kkm,resp)
    return result


def is_valid_link(kkm_link):
    valid_prefix = f'{baseurl}/kkm/transactions/details/'
    return kkm_link.startswith(valid_prefix)

def getdocumentstatus(url):
    kkm, resp, document,salon_id = getdata(url)
    print(document)
    bpsatatus = {
        1: "Статус 1 - не напечатан чек",
        2: "Статус 2 - печатается чек продажи",
        3: "Статус 3 - напечатан чек продажи",
        4: "Статус 4 - печатается чек возврата",
        5: "Статус 5 - напечатан чек возврата"
    }
    url = f"{baseurl}/api/v1/company/{salon_id}/sale/{document}"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    print(response)
    bps = response["data"]["kkm_state"]["transactions"][0]["document"]["bill_print_status"]
    return bpsatatus.get(bps)


def generate_payload(kkm_id,kkm_response):
    global warning
    warning = 0
    if "CheckNumber" in kkm_response:
        check = kkm_response["CheckNumber"]
    else:
        check = ""
        warning = 1

    if "SessionNumber" in kkm_response:
        session = kkm_response["SessionNumber"]
    else:
        session = ""
        warning = 1

    url = f"{baseurl}/api/v1/kkm_transactions/{kkm_id}/save_result"
    payload = json.dumps({
        "kkm_transaction_id": kkm_id,
        "result_check_number": check,
        "result_session_number": session,
        "status": 0,
        "error": "",
        "type": "sale",
        "sessionState": 0,
        "kkm_response": kkm_response
    })
    # response = requests.request("POST", url, headers=headers, data=payload).json()
    print(payload)
    return payload, warning



def execute_force(kkm_id,kkm_response):
    if "CheckNumber" in kkm_response:
        check = kkm_response["CheckNumber"]
    else:
        check = ""

    if "SessionNumber" in kkm_response:
        session = kkm_response["SessionNumber"]
    else:
        session = ""
    url = f"{baseurl}/api/v1/kkm_transactions/{kkm_id}/save_result"
    payload = json.dumps({
        "kkm_transaction_id": kkm_id,
        "result_check_number": check,
        "result_session_number": session,
        "status": 0,
        "error": "",
        "type": "sale",
        "sessionState": 0,
        "kkm_response": kkm_response
    })
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response