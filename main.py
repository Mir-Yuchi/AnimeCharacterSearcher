import time

import requests

API_BASE_URl = "https://api.jikan.moe/v4/"
API_CHARACTERS_BASE_URL = API_BASE_URl + "characters/"


def get_all_characters(page_number: int = 1) -> dict | tuple:
    response = requests.get(API_CHARACTERS_BASE_URL, params={"page": page_number})
    return response.json() if response.status_code == 200 else response.status_code


def get_character_detail(character_id: int):
    response = requests.get(f"{API_CHARACTERS_BASE_URL}{character_id}/full")
    return response.json() if response.status_code == 200 else response.status_code


def anime_character_searcher():
    character_name = input("Введите имя аниме персонажа: ")
    counter = 1
    all_characters = []
    part_characters = get_all_characters()
    if isinstance(part_characters, int):
        print("Часть персонажей не получена! Проблема с сетью", part_characters)
        return
    all_characters.extend(part_characters['data'])
    while part_characters["pagination"]["has_next_page"]:
        if counter == 100:
            print("Всё! Полномочий БД на этом всё!")
            break
        print("Есть след. страница")
        counter += 1
        part_characters = get_all_characters(counter)
        if isinstance(part_characters, int):
            print("Часть персонажей не получена! Проблема с сетью", part_characters)
            break
        all_characters.extend(part_characters['data'])
        print("Добавил в общ. список")
        print("Текущая страница:", counter)
        time.sleep(2)
    found_characters = []
    for character_obj in all_characters:
        if character_name in character_obj["name"].lower():
            found_characters.append(character_obj)
    print(f"Найдены {len(found_characters)} персонажей")
    if not found_characters:
        print("Персонажей не найдено!")
        return
    print("Выберите персонажа из возможных вариантов:\n")
    for id_, character_obj in enumerate(found_characters, start=1):
        print(f"{id_}: {character_obj['name']}, Ссылка на фото: {character_obj['images']['jpg']['image_url']}")
    num = int(input("Введите id персонажа: "))
    character = found_characters[num - 1]
    character_detail = get_character_detail(character["mal_id"])
    if isinstance(character_detail, int):
        print("Не получилось получить подробную инфу", character_detail)
        return
    print(f"{character_detail['data']['name']} - {character_detail['data']['name_kanji']}\n"
          f"Аниме на которым этот персонаж участвовал:\n"
          f"{', '.join(map(lambda obj: 'Роль: ' + obj['role'] + ' Аниме: ' + obj['anime']['title'], character_detail['data']['anime']))}")


anime_character_searcher()
