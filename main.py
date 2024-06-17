import requests
import os
import json
from tqdm import tqdm

class VK:
    def __init__(self, token_vk, user_id):
        self.token = token_vk
        self.user_id = user_id

    def get_photos(self, count=5):
        params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': count,
            'v': '5.199'
        }
        headers = {'Authorization': 'Bearer ' + self.token}
        response = requests.get('https://api.vk.com/method/photos.get', params=params, headers=headers)
        return response.json()

class YandexDisk:
    def __init__(self, token_ya):
        self.token = token_ya

    def create_folder(self, folder_name):
        headers = {'Authorization': 'OAuth ' + self.token}
        requests.put(f'https://cloud-api.yandex.net/v1/disk/resources?path={folder_name}', headers=headers)

    def upload_photo(self, folder_name, file_name, url_photo):
        headers = {'Authorization': 'OAuth ' + self.token}
        params = {'path': f'{folder_name}/{file_name}', 'url': url_photo}
        response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', params=params, headers=headers)
        return response.status_code

    def save_photos_info(self, folder_name, photos_info):
        with open(f'{folder_name}/photos_info.json', 'w') as file:
            json.dump(photos_info, file, ensure_ascii=False, indent=4)

# Использование классов
token_vk = 'ВАШ_ТОКЕН_VK'
user_id = 'ID_ПОЛЬЗОВАТЕЛЯ'
vk = VK(token_vk, user_id)

token_ya = 'ВАШ_ТОКЕН_YANDEX'
folder_name = 'VK_Photos'
ya_disk = YandexDisk(token_ya)

# Создаем папку на Я.Диске
ya_disk.create_folder(folder_name)

photos_info = vk.get_photos()
if 'response' in photos_info:
    photos = photos_info['response']['items']
    photos.sort(key=lambda x: max(x['sizes'], key=lambda size: size['width'] * size['height'])['width'] * max(x['sizes'], key=lambda size: size['width'] * size['height'])['height'], reverse=True)
    photos = photos[:5]  # Ограничиваем количество фотографий до 5

    for item in tqdm(photos, desc='Загрузка фотографий'):
        max_size_photo = max(item['sizes'], key=lambda size: size['width'] * size['height'])
        file_name = str(item['likes']['count']) + '.jpg'
        ya_disk.upload_photo(folder_name, file_name, max_size_photo['url'])

    # Сохраняем информацию о фотографиях в JSON-файл
    ya_disk.save_photos_info(folder_name, photos)

print('Фотографии загружены на Яндекс.Диск и информация сохранена в JSON-файл.')
