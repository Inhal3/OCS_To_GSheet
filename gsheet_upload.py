import json
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account


def sheet_upload():

    """
    This module making our margin on items from "json/goods.json" and uploading them to google sheets
    Example - https://docs.google.com/spreadsheets/d/1JtPgCSjIckcOkcrure7_GLJej3r5Q2pRgtaILJpXOr0/edit?usp=sharing
    """

    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    service_account_file = 'cfg/google_credentials.json'
    spreadsheet_id = '1JtPgCSjIckcOkcrure7_GLJej3r5Q2pRgtaILJpXOr0'
    sheet_range = 'Товары'

    start = time.time()

    credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)

    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    result = service.get(spreadsheetId=spreadsheet_id,
                         range=sheet_range).execute()

    sheet_range = 'Товары!A2:D20000'

    with open('json/goods.json', encoding='utf-8') as f:
        items = json.load(f)
        f.close()

    category_ids = list(items.keys())
    array = {'values': []}

    for i in category_ids:
        sku = i
        category_name = items[i]['categoryName']
        item_name = items[i]['itemName']
        price = items[i]['Price']

        array['values'].append([sku, category_name, item_name, price])

    service.update(spreadsheetId=spreadsheet_id,
                   range=sheet_range,
                   valueInputOption='RAW',
                   body=array).execute()

    end_time = str(time.time() - start)[:4:]

    print(f'\n'
          f'Таблица обновлена.\n'
          f'Затраченное время {end_time}')
