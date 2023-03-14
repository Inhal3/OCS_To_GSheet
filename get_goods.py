import requests
import json
import time
from cfg.ocs_token import token
from cfg.margin_ratio import margin


def get_items():
    """
    This module gets all goods from api of b2b.ocs.ru and transforms it to
    json file "json/goods.json"
    """

    start = time.time()
    print('Выгрузка началась')

    items_response = requests.get(f'https://connector.b2b.ocs.ru/api/v2/catalog/categories/'
                                  f'all/products'
                                  f'?shipmentcity=Москва'
                                  f'&onlyavailable=true'
                                  f'&includeregular=true'
                                  f'&includesale=true'
                                  f'&includeuncondition=false'
                                  f'&includeunconditionalimages=false'
                                  f'&includemissing=false'
                                  f'&withdescriptions=false',
                                  headers={'accept': 'application/json',
                                           'X-API-Key': token}).json()

    rate_response = requests.get('https://connector.b2b.ocs.ru/api/v2/account/currencies/exchanges',
                                 headers={'X-API-Key': token}).json()

    usd_rate = int(rate_response[0]['rate'])
    eur_rate = int(rate_response[1]['rate'])

    goods = {}

    for i in range(0, len(items_response['result'])):
        item_id = items_response['result'][i]['product']['itemId']
        item_name = items_response['result'][i]['product']['itemName']

        try:
            category_name = items_response['result'][i]['product']['catalogPath'][-1]['name']
        except IndexError:
            category_name = 'Без категории'

        currency = items_response['result'][i]['price']['priceList']['currency']
        price = int(items_response['result'][i]['price']['priceList']['value'])

        if currency == 'USD':
            goods[item_id] = {'categoryName': category_name,
                              'itemName': item_name,
                              'Price': (price * usd_rate) + (price * usd_rate * margin)}
        elif currency == 'EUR':
            goods[item_id] = {'categoryName': category_name,
                              'itemName': item_name,
                              'Price': (price * eur_rate) + (price * eur_rate * margin)}
        elif currency == 'RUR':
            goods[item_id] = {'categoryName': category_name,
                              'itemName': item_name,
                              'Price': price + (price * margin)}

    with open('json/goods.json', 'w', encoding='utf-8') as f:
        json.dump(goods, f, ensure_ascii=False, indent=2)
        f.close()
    end = str(time.time() - start)[:2:]
    print(f'Выгрузка закончилась\n'
          f'Затраченное время - {end} сек.')
