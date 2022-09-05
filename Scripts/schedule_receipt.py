import os
import requests
from bs4 import BeautifulSoup
from file_names import *
from configure import path_to_save

urls = {
    'main': 'https://www.sevsu.ru/upload/iblock/f3a/41ws2acavp11ywtjbnnyosix3cuumlta/2_kurs_IITUTS.xlsx',
    'pul': 'https://www.sevsu.ru/upload/iblock/fd0/ixkrqs052h3tkgrlejqee2ylntnsv51p/pul.xlsx',
    'fiz': 'https://www.sevsu.ru/'
}

sch_page = 'https://www.sevsu.ru/univers/shedule/'


def have_file(key):
    return os.path.isfile(path_to_save + schedules[key])


def download_file(key):
    downloaded_file = requests.get(urls[key])
    with open(path_to_save + schedules[key], 'wb') as file:
        file.write(downloaded_file.content)


def need_to_update(key):
    result = requests.get(sch_page).content
    soup = BeautifulSoup(result, 'html.parser')

    target_word = '2 курс ИИТУТС' if key == 'main' else 'pul'

    for url_text in soup.find_all('a'):
        url = url_text.get('href')

        if target_word in url and 'Магистратура' not in url:
            base = urls[key][:35]
            current = urls[key][35:]
            acquired = url[15:]

            if acquired != current:
                urls[key] = base + acquired
                return True
    return False


def prepare(key):
    print('Old link: ' + urls[key])
    if not have_file(key) or need_to_update(key):
        download_file(key)
        print('Schedule has been updated!')
    print('New link: ' + urls[key])
    return path_to_save + schedules[key]
