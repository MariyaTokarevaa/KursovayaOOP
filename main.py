import requests
import json
import os
from tqdm import tqdm

class VK:

    def __init__(self, access_token, my_id, version='5.199'):
        self.token = access_token
        self.id = my_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_photos(self, offset=0, count=50):

        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': my_id,
                    'album_id': 'profile',
                    'access_token': access_token,
                    'v': '5.199',
                    'extended': '1',
                    'photo_sizes': '1',
                    'count': count,
                    'offset': offset
                    }
        res = requests.get(url=url, params=params)
        return res.json()

    def get_all_photos(self):
        data = self.get_photos()
        all_photo_count = data['response']['count']  # Количество всех фотографий профиля
        i = 0
        count = 50
        photos = []  # Список всех загруженных фото
        max_size_photo = {}  # Словарь с парой название фото - URL фото максимального разрешения

        # Создаём папку на компьютере для скачивания фотографий
        if not os.path.exists('images_vk'):
            os.mkdir('images_vk')

        while i <= all_photo_count:
            if i != 0:
                data = self.get_photos(offset=i, count=count)

            # Проходимся по всем фотографиям
            for photo in data['response']['items']:
                max_size = 0
                photos_info = {}
                # Выбираем фото максимального разрешения и добавляем в словарь max_size_photo
                for size in photo['sizes']:
                    if size['height'] >= max_size:
                        max_size = size['height']
                if photo['likes']['count'] not in max_size_photo.keys():
                    max_size_photo[photo['likes']['count']] = size['url']
                    photos_info['file_name'] = f"{photo['likes']['count']}.jpg"
                else:
                    max_size_photo[f"{photo['likes']['count']} + {photo['date']}"] = size['url']
                    photos_info['file_name'] = f"{photo['likes']['count']}+{photo['date']}.jpg"

                # Формируем список всех фотографий для дальнейшей упаковки в .json

                photos_info['size'] = size['type']
                photos.append(photos_info)

            # Скачиваем фотографии
            for photo_name, photo_url in max_size_photo.items():
                with open('images_vk/%s' % f'{photo_name}.jpg', 'wb') as file:
                    img = requests.get(photo_url)
                    file.write(img.content)

            print(f'Загружено {len(max_size_photo)} фото')
            i += count

        # Записываем данные о всех скачанных фоторафиях в файл .json
        with open("photos.json", "w") as file:
            json.dump(photos, file, indent=4)

    def start():
        try:
            my_id = input('Введите ID пользователя ВКонтакте: ')
            vk = vk(access_token, my_id)
            screen_name = vk.users_info()['response'][0]['screen_name']
            id1 = str(vk.users_info()['response'][0]['id'])

            if my_id == screen_name or my_id == id1:
                print('Фото будут загружены из профиля пользователя с именем: ')
                print(vk.users_info()['response'][0]['first_name'])


        except IndexError:
            print('Неверный ID, попробуйте снова')
        except UnboundLocalError:
            print('Неверный ID, попробуйте снова')
            my_id = id1
        return my_id

    my_id = start()
    vk = VK(access_token, my_id)

    token_ya = input('Введите токен с Полигона Яндекс.Диска: ')

class Yandex:
   def __init__(self, token_ya):
       self.token = token_ya

   # Создаем папку на Яндекс.Диске
   def create_folder(self):
       params = {'path': 'Images_vk'}
       headers = {'Authorization': 'OAuth ' + self.token}
       response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                               params=params,
                               headers=headers)
       return 'Папка на Яндекс.Диске создана'

   # Загружаем фото на Яндекс.Диск
   def upload_photos(self):
       a = vk.get_file_name()
       b = vk.get_photo_url()

       for file_name, url_photo in zip(a, b):
           params = {'path': f'Images_vk/{file_name}', 'url': f'{url_photo}'}
           headers = {'Authorization': 'OAuth ' + self.token}
           response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                    params=params,
                                    headers=headers)
       return "Фотографии уже загружены"

   ya = Yandex(token_ya)

if __name__ == '__main__':

    print(ya.create_folder())
    print(ya.upload_photos())
    with open('save_file.json') as f: # Загрузка файла
        res = f.read()
    print(res)

