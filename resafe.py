import json
from config import headers
import requests
from tqdm import tqdm
import logging

# salon = 162492
# salon = 543449
# salon = 490978


logging.basicConfig(filename='resafe.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
def getshedule(salon):
    logging.info(f"Старт getshedule")
    staff_url = f"https://api.yclients.com/api/v1/company/{salon}/staff/"
    response = requests.request("GET", staff_url, headers=headers).json()
    staff = [item["id"] for item in tqdm(response["data"], desc='GETTING STAFF')]
    logging.info(f"Получили сотрудников ({len(staff)}). Список: {staff}")
    data = []
    for item in tqdm(staff, desc='GETTING SHEDULE'):
        get_shedule_url = f"https://api.yclients.com/api/v1/schedule/{salon}/{item}/2023-06-01/2024-01-31"
        response = requests.request("GET", get_shedule_url, headers=headers).json()
        logging.info(f"Получили расписание сотрудника {item} : {response['success']}, длина: {len(response['data'])}")
        data.append({
            "staff": item,
            "shedule": response["data"]
        })
    return data

def resafe(salon):

    data = getshedule(salon)
    for item in tqdm(data, desc="PUTTING SHEDULE"):
        put_shedule_url = f"https://api.yclients.com/api/v1/schedule/{salon}/{item['staff']}"
        payload = json.dumps(item['shedule'])
        response = requests.request("PUT", put_shedule_url, headers=headers, data=payload).json()
        logging.info(f"Сохранили расписание сотрудника {item['staff']} : , ответ: {response}")
