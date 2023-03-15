# This module not used yet

from cfg.ocs_token import token
import requests
import json


def categories():

    """
    This module gets maximum nested categories from b2b.ocs.ru
    and transforming them to json/categories.json
    """

    # Getting raw categories list
    category_tree = requests.get("https://connector.b2b.ocs.ru/api/v2/catalog/categories",
                                 headers={'X-API-Key': token}).json()

    category_name_id = []
    category_names = []

    # Transforming raw categories list to 'json/categories.json'
    for a in range(0, len(category_tree)):
        for b in range(0, len(category_tree[a]['children'])):
            if len(category_tree[a]['children'][b]['children']) > 0:
                for c in range(0, len(category_tree[a]['children'][b]['children'])):
                    category_name_id.append(category_tree[a]['children'][b]['children'][c]['category'])
                    category_names.append(category_tree[a]['children'][b]['children'][c]['name'])
            else:
                category_name_id.append(category_tree[a]['children'][b]['category'])
                category_names.append(category_tree[a]['children'][b]['name'])

    category_dict = {}
    for i in range(0, len(category_name_id)):
        category_dict[category_name_id[i]] = category_names[i]

    with open('json/categories.json', 'w', encoding='utf-8') as f:
        json.dump(category_dict, f, ensure_ascii=False, indent=1)
        f.close()
