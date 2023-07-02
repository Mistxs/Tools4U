import json
from config import headers
import requests
from tqdm import tqdm
import logging

salon = 162492
# salon = 543449

data = []

logging.basicConfig(filename='resafe.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
def getshedule():
    logging.info(f"Старт getshedule")
    staff_url = f"https://api.yclients.com/api/v1/company/{salon}/staff/"
    response = requests.request("GET", staff_url, headers=headers).json()
    staff = [item["id"] for item in tqdm(response["data"], desc='GETTING STAFF')]
    logging.info(f"Получили сотрудников ({len(staff)}). Список: {staff}")
    for item in tqdm(staff, desc='GETTING SHEDULE'):
        get_shedule_url = f"https://api.yclients.com/api/v1/schedule/{salon}/{item}/2023-06-01/2023-12-31"
        response = requests.request("GET", get_shedule_url, headers=headers).json()
        logging.info(f"Получили расписание сотрудника {item} : {response['success']}, длина: {len(response['data'])}")
        data.append({
            "staff": item,
            "shedule": response["data"]
        })

def resafe():
    for item in tqdm(data, desc="PUTTING SHEDULE"):
        put_shedule_url = f"https://api.yclients.com/api/v1/schedule/{salon}/{item['staff']}"
        payload = json.dumps(item['shedule'])
        response = requests.request("PUT", put_shedule_url, headers=headers, data=payload).json()
        logging.info(f"Сохранили расписание сотрудника {item['staff']} : , ответ: {response}")
