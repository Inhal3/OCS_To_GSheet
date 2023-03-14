import json
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account


def sheet_upload():

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'C:\PythonProjects\OCS_To_GSheet\cfg\google_credentials.json'
    SAMPLE_SPREADSHEET_ID = '1JtPgCSjIckcOkcrure7_GLJej3r5Q2pRgtaILJpXOr0'
    SAMPLE_RANGE_NAME = 'Товары'

    start = time.time()

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    result = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                         range=SAMPLE_RANGE_NAME).execute()

    sheet_range = 'Товары!A2:D20000'

    with open('C:\PythonProjects\OCS_To_GSheet\json\goods.json', encoding='utf-8') as f:
        items = json.load(f)
        f.close()

    category_ids = list(items.keys())
    array = {'values': []}

    for i in category_ids:
        SKU = i
        category_name = items[i]['categoryName']
        item_name = items[i]['itemName']
        price = items[i]['Price']

        array['values'].append([SKU, category_name, item_name, price])

    service.update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                   range=sheet_range,
                   valueInputOption='RAW',
                   body=array).execute()

    end_time = str(time.time() - start)[:4:]

    print(f'\n'
          f'Таблица обновлена.\n'
          f'Затраченное время {end_time}')
