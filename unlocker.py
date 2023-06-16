import re

from flask import Blueprint, request
from bs4 import BeautifulSoup
import requests

from config import auth_cookie, headers, testerhead

unlocker = Blueprint('unlocker', __name__)



@unlocker.route('/unlock', methods=['POST'])
def unlock():
    record_link = request.json['record_link']
    print(record_link)
    if validate_record_link(record_link):
        link_type, link_result = validate_record_link(record_link)
        if link_type == 'rec':
            rec_id = extract_record_id(link_result)
            response = send_post_request(rec_id)
            return response.text
        elif link_type == 'kkm':
            salon_id, document_id = getdata(link_result)
            record_id = getrecid(salon_id,document_id)
            response = send_post_request(record_id)
            return response.text
    else:
        return "Ссылка имеет некорректный формат, пожалуйста, проверьте"


@unlocker.route('/details', methods=['POST'])
def getinfo():
    record_link = request.json['record_link']
    if validate_record_link(record_link):
        link_type, link_result = validate_record_link(record_link)
        if link_type == 'rec':
            return "У вас ссылка на запись. Информацию об операции печати чека вы легко можете получить из ERP"
        elif link_type == 'kkm':
            salon_id, document_id = getdata(link_result)
            record_id = getrecid(salon_id,document_id)
            return f"Ссылка на запись: <a target = _blank href = 'https://yclients.com/timetable/{salon_id}#main_date=2023-05-24&open_modal_by_record_id={record_id}'>https://yclients.com/timetable/{salon_id}#main_date=2023-05-24&open_modal_by_record_id={record_id}</a>"
    else:
        return "Ссылка имеет некорректный формат, пожалуйста, проверьте"


def getdata(url):
    response = requests.get(url, cookies={"Cookie": auth_cookie})
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        ibox_contents = soup.find_all("div", class_="ibox-content")
        td_elements = soup.find("table", class_="table").find_all("td")
        document_id = td_elements[1].get_text(strip=True)
        li_element = soup.find("li", class_="calendar-toggle")
        a_element = li_element.find("a")
        href_value = a_element.get("href")
        salon_id = href_value.split("/timetable/")[1]
        return salon_id, document_id

    else:
        print("Ошибка при выполнении запроса:", response.status_code)


def getrecid(salon,doc):
    url = f"https://yclients.com/api/v1/company/{salon}/sale/{doc}"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    fintrans = response["data"]["state"]["payment_transactions"][0]["id"]
    findata = requests.get(f"https://api.yclients.com/api/v1/finance_transactions/{salon}/{fintrans}", headers=headers).json()
    rec_id = findata["data"]["record_id"]
    return rec_id

def validate_record_link(link):
    record_pattern = r'https://yclients.com/timetable/\d+#main_date=\d{4}-\d{2}-\d{2}&open_modal_by_record_id=\d+'
    kkm_pattern = r'https://yclients.com/kkm/transactions/details/(\d+)/'

    record_match = re.match(record_pattern, link)
    kkm_match = re.match(kkm_pattern, link)
    print("vrl: ", link)
    if record_match:
        return 'rec', record_match.group()  # Возвращаем тип 'rec' и ссылку на визит
    elif kkm_match:
        return 'kkm', kkm_match.group()  # Возвращаем тип 'kkm' и kkm_link
    else:
        return False  # Ссылка не соответствует ни одному из шаблонов

def extract_record_id(record_link):
    return record_link.split('open_modal_by_record_id=')[1]

def send_post_request(rec_id):
    url = f'https://yclients.com/tester/unlock_record/{rec_id}'
    headers = testerhead
    print(url)
    response = requests.post(url, headers=headers)
    return response
