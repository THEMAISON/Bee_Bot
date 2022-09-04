import requests
from bs4 import BeautifulSoup
from configure import path_to_save

sch_page = 'https://www.sevsu.ru/univers/shedule/'


def check_for_updates(key):
    result = requests.get(sch_page).content
    soup = BeautifulSoup(result, 'html.parser')

    for url_text in soup.find(class_='document-link__group').find_all('a'):
        url = url_text.get('href')

        if '2_kurs_IITUTS' in url:
            base = link['schedule'][:72]
            current = link['schedule'][72:]
            acquired = url[52:]

            if acquired != current:
                link['schedule'] = base + acquired
                return True
    return False

