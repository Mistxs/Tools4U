import json
import re

from flask import Blueprint, request, jsonify
from bs4 import BeautifulSoup
from config import auth_cookie, headers
from datetime import datetime
import requests
import dateparser


superloya = Blueprint('superloya', __name__)
chain = 1

@superloya.route('/superloyal', methods=['POST'])
def getdata():
    cardlink = request.json['cardlink']
    if validate_link(cardlink):

        link_type, link_result = validate_link(cardlink)
        if link_type == 'card':
            t1, t2, t3 = parsepage(link_result)
            return jsonify({'table1': t1, 'table2': t2, 'table3': t3})
        elif link_type == 'abon':
            t1, t2, t3 = parsepageabon(link_result)
            return jsonify({'table1': t1, 'table2': t2, 'table3': t3})
    else:
        return "Ссылка имеет некорректный формат, пожалуйста, проверьте"


def validate_link(link):
    global chain
    card_pattern = r'https://yclients.com/group_loyalty_cards/show/\d+/\d+'
    abon_pattern = r'https://yclients.com/group_loyalty_abonements/show/\d+/\d+'
    card_match = re.match(card_pattern, link)
    abon_match = re.match(abon_pattern, link)
    if card_match:
        chain = link.split("/")[-2]
        return 'card', card_match.group()
    elif abon_match:
        chain = link.split("/")[-2]
        return 'abon', abon_match.group()
    else:
        return False  # Ссылка не соответствует ни одному из шаблонов

def getTypesCard(name):
    global chain
    url = f"https://api.yclients.com/api/v1/chain/{chain}/loyalty/card_types"
    response = requests.request("GET", url, headers=headers).json()
    for item in response["data"]:
        if item["title"] == name:
            return item["id"]

def parsepage(url):
    print(url)
    response = requests.get(url, cookies={"Cookie": auth_cookie})
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        info = []
        tbody = soup.find('table', class_='clients-table')
        for row in tbody.find_all('tr'):
            name = row.find('td').get_text(strip=True)
            data = row.find('td').find_next('td').get_text(strip=True)
            info.append({
                "name": name,
                "data": data
            })
        namecard = info[1]["data"]
        print(namecard)
        id = getTypesCard(namecard)
        info[1]["data"] = f'<a target=_blank href="https://yclients.com/group_loyalty_card_types/edit/{chain}/{id}">{namecard}</a>'


        main = []
        tbody = soup.find_all('table', class_='clients-table')
        for row in tbody[1].find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 5:
                program_id = cells[0].get_text(strip=True)
                program = cells[1].get_text(strip=True)
                type = cells[2].get_text(strip=True)
                collect = cells[3].get_text(strip=True)
                amount = cells[4].get_text(strip=True)

                main.append({
                    "number": program_id,
                    "name": f'<a target=_blank href="https://yclients.com/group_loyalty_programs/edit/{chain}/{program_id}">{program}</a>',
                    "type": type,
                    "collect": collect,
                    "amount": amount
                })

        data = []
        tbody = soup.find('tbody', class_='info-table')

        # Итерируемся по каждой строке таблицы, исключая последние две строки (Баланс и Скидки)
        for row in tbody.find_all('tr', class_='client-box success'):
            transaction_id = row.find('td').get_text(strip=True)
            create_date = row.find('td').find_next('td').get_text(strip=True)
            type_ = row.find('td').find_next('td').find_next('td').get_text(strip=True)
            actions = row.find('td').find_next('td').find_next('td').find_next('td').get_text(strip=True)
            amount = row.find('td').find_next('td').find_next('td').find_next('td').find_next('td').get_text(strip=True)


            data.append({
                "transaction_id": transaction_id,
                "create_date": create_date,
                "type": type_,
                "actions": actions,
                "amount": amount,
            })


        getLoyaltyTransaction(data)
        return info, main, data

def parsepageabon(url):
    response = requests.get(url, cookies={"Cookie": auth_cookie})
    if response.status_code == 200:
        html_content = response.text
        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(html_content, "html.parser")
        tbody = soup.find('table', class_='clients-table')
        # Находим первый элемент <td>
        td_element = soup.find('td', text='Тип')
        # Находим следующий элемент <a> после <td>
        link_element = td_element.find_next('a')
        # Получаем значение атрибута href
        abonlink = link_element.get('href')

        # забираем общую информацию
        info = []
        tbody = soup.find('table', class_='clients-table')
        for row in tbody.find_all('tr'):
            name = row.find('td').get_text(strip=True)
            data = row.find('td').find_next('td').get_text(strip=True)
            info.append({
                "name": name,
                "data": data
            })
        namecard = info[2]["data"]
        info[2]["data"] = f'<a target=_blank href="https://yclients.com{abonlink}">{namecard}</a>'

        main = []

        data = []
        # Находим tbody в таблице операций лояльности
        tbody = soup.find('tbody', class_='info-table')

        # Итерируемся по каждой строке таблицы, исключая последние две строки (Баланс и Скидки)
        for row in tbody.find_all('tr', attrs={'data-locator': 'abonement_transactions_table_row'}):
            transaction_id = row.find('td').get_text(strip=True)
            create_date = row.find('td').find_next('td').get_text(strip=True)
            type_ = row.find('td').find_next('td').find_next('td').get_text(strip=True)
            actions = row.find('td').find_next('td').find_next('td').find_next('td').get_text(strip=True)
            amount = row.find('td').find_next('td').find_next('td').find_next('td').find_next('td').get_text(strip=True)


            data.append({
                "transaction_id": transaction_id,
                "create_date": create_date,
                "type": type_,
                "actions": actions,
                "amount": amount,
            })


        getAbonementTransaction(data)
        return info, main, data



def convert_date(date_string):
    input_format = "d MMMM yyyy в HH:mm"
    date_obj = dateparser.parse(date_string, languages=['ru'], date_formats=[input_format])
    output_format = "%Y-%m-%d"
    formatted_date = date_obj.strftime(output_format)
    return formatted_date

def getvisit(id):
    url = f"https://api.yclients.com/api/v1/visits/{id}"
    response = requests.request("GET", url, headers=headers).json()
    date_string = response["data"]["datetime"]
    datetime_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
    date = datetime_obj.strftime("%Y-%m-%d %H:%M")
    record_id = response["data"]["records"][0]["id"]
    salon_id = response["data"]["records"][0]["company_id"]
    return date, record_id, salon_id


def getLoyaltyTransaction(data):
    url = f"https://api.yclients.com/api/v1/chain/{chain}/loyalty/transactions"
    for item in data:
        date = convert_date(item["create_date"])
        payload = json.dumps({
            "created_after": date,
            "created_before": date,
            "count": "1000"
        })
        response = requests.request("GET", url, headers=headers, data=payload).json()
        for transaction in response["data"]:
            if int(item["transaction_id"]) == int(transaction['id']):
                item["visit_id"] = transaction['visit_id']
                date, record, salon = getvisit(transaction['visit_id'])
                item["program_id"] = transaction['program_id']
                dateforlink = date.split(" ")[-2]
                item["record_id"] = record
                actions_link = f'<a target=_blank href="https://yclients.com/group_loyalty_programs/edit/{chain}/{item["program_id"]}">{item["actions"]}</a>'
                date_link = f'<a target=_blank href="https://yclients.com/timetable/{salon}#main_date={dateforlink}&open_modal_by_record_id={item["record_id"]}">{date}</a>'
                item["actions"] = actions_link
                item["date"] = date_link

def getAbonementTransaction(data):
    print("getdata started")
    print(data)
    url = f"https://api.yclients.com/api/v1/chain/{chain}/loyalty/transactions"
    for item in data:
        date = convert_date(item["create_date"])
        payload = json.dumps({
            "created_after": date,
            "created_before": date,
            "count": "1000"
        })
        response = requests.request("GET", url, headers=headers, data=payload).json()
        for transaction in response["data"]:
            if int(item["transaction_id"]) == int(transaction['id']):
                item["visit_id"] = transaction['visit_id']
                date, record, salon = getvisit(transaction['visit_id'])
                item["program_id"] = transaction['program_id']
                dateforlink = date.split(" ")[-2]
                item["record_id"] = record
                actions_link = f'<a target=_blank href="https://yclients.com/group_loyalty_programs/edit/{chain}/{item["program_id"]}">{item["actions"]}</a>'
                date_link = f'<a target=_blank href="https://yclients.com/timetable/{salon}#main_date={dateforlink}&open_modal_by_record_id={item["record_id"]}">{date}</a>'
                item["actions"] = actions_link
                item["date"] = date_link
        print(response)
        print(data)


