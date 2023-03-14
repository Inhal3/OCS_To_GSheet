# This module no longer used


def categories():
    from cfg.ocs_token import token
    import requests
    import json

    # Получаем сырой список категорий
    category_tree = requests.get("https://connector.b2b.ocs.ru/api/v2/catalog/categories",
                                 headers={'X-API-Key': token}).json()

    category_name_id = []
    category_names = []

    # Поучаем лист с названиями и ID максимально вложенных категорий
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
