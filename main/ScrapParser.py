"""
:copyright: (c) 2022 by Sergey Cheh.
:license: Apache2, see LICENSE for more details.
"""


import time
import csv

from random import randint

import requests

from bs4 import BeautifulSoup as BSoup

HEADERS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Opera/9.80 (Windows NT 6.2; WOW64) Presto/2.12.388 Version/12.17"
]


def get_html(url, headers):
    """ Возвращает объект Response из библиотеки requests и представляет как текст """
    headers = {"user-agent":HEADERS[randint(0,2)]}
    try:
        requested_html = requests.get(url, headers=headers)
        return requested_html.text
    except:
        print(requested_html.status_code)
        return requested_html.status_code
    

def parse_dict(html):
    """Функция принимает результат объект requests.models.Response()
    представленный как текст, после чего инициализируется переменная под
    объект BeautyfulSoup с соответствующим параметром 'lxml' и создаётся
    ещё одна переменная t_ads которая взвращает целочисленный ответ
    с общимколичеством объявлений
    """
    parsed_vars = {}
    try:
        soup = BSoup(html, 'lxml')
        t_ads = soup.find('span', class_='page-title-count-wQ7pG').text
        pages = soup.find('div', class_='pagination-pages').find_all('a', \
            class_='pagination-page')[-1].get('href')
        total_pages = pages.split('=')[1].split('&')[0]
        parsed_vars["TOTAL_PAGES"] = int(total_pages)
        parsed_vars["TOTAL_ADS"] =int(t_ads.replace('\xa0',''))
        return parsed_vars
    except:
        message = "Поздравляю, 429 ошибка"
        return  message
    


def write_csv(data):
    """ Запись собранных файлов в файл """
    with open('parsed_data.csv', \
            encoding="utf-8", mode="a") as parsed_data_file:
        writer = csv.writer(parsed_data_file)
        writer.writerow( (data['title'],
                          data['url'],
                          data['price'],
                          data['category'],
                          ) )

def get_page_data(html):
    """ Получение информации для построчной записи файл данных из объявления 
    ads - список объявлений
    Пошаговая логика:
    1) ищем родной блок каталог (тот что не является extra, с атрибутом "data-marker")
    2) ищем все ad
    3) записываем все ad в ads
    type(ads) -> ResultSet
    type(ads[1]) -> tag

    Эта функция собирает данные из каждого объявления
    """
    soup = BSoup(html, 'lxml')

    
    ads = soup.find('div', class_='items-items-kAJAg',
        attrs={"data-marker": "catalog-serp"}).find_all('div', class_='iva-item-root-_lk9K')
    for ad in ads:
        # title,url, postday,
        try:
            title = ad.find('div', class_='iva-item-titleStep-pdebR').find('h3').text
        except:
            title = 'Без заголовка'

        try:
            url ='https://wwww.avito.ru' + ad.find('div' ,
                class_='iva-item-titleStep-pdebR').find('a').get('href')
        except:
            url = 'Null'

        try:
            price = ad.find('div',
                class_='iva-item-priceStep-uq2CQ').find('span', class_='price-text-_YGDY').text
        except:
            price = 'Не указана'

        try:
            category = ad.find('div', attrs={"data-marker": "item-line"}).find('span').text
        except:
            category = 'не определена'

        data = {'title': title,
                'url': url,
                'price': price,
                'category': category,
                }

        write_csv(data)


def scrap_parse(url='',headers=HEADERS):
    """Собрал функцию  для парсинга"""

    PAGE_PART = '?p='
    html = get_html(url,headers)
    PARSED_DICT = parse_dict(html)

    ads_in_url = PARSED_DICT["TOTAL_ADS"]

    if ads_in_url <= 50:
        print(str(ads_in_url) + ' объявления, выгружаю...')
        get_page_data(html)
    else:
        print(str(ads_in_url) + ' предложений. Расчет страниц, прогружаю объявления...')
        total_pages = PARSED_DICT["TOTAL_PAGES"]
        for num_page in range(1, total_pages + 1):
            print("Смотрю страницу:",num_page)
            url_gen = url + PAGE_PART + str(num_page)

            html_qset = get_html(url_gen, headers)
            get_page_data(html_qset)
            time.sleep(1)
    print("Вывод готов в текущей дериктории")


def main():
    pass

if __name__ == '__main__':
    main()
