# Добавить лицензию
# Авторство копирайт и дт
""" Документация """

import time
import csv

import requests

from bs4 import BeautifulSoup as BSoup



#  1) How many total ads n region?
#  2) How  many pages
#  3) Do a list with pages urls
#  4) collect data
#  5) get total pages, работает корректно если t_ads > 50!!!
#  6) додумать логику при t_ads < 50, когда есть extra


TARGET_URL = 'https://www.avito.ru/bikin/telefony'


def get_html(url):
    """ Возвращает объект Response из библиотеки requests и представляет как текст """
    requested_html = requests.get(url)
    return requested_html.text

def total_ads(html):
    """Функция принимает результат объект requests.models.Response()
    представленный как текст, после чего инициализируется переменная под
    объект BeautyfulSoup с соответствующим параметром 'lxml' и создаётся
    ещё одна переменная t_ads которая взвращает целочисленный ответ
    с общимколичеством объявлений
    """
    soup = BSoup(html, 'lxml')
    t_ads = soup.find('span', class_='page-title-count-wQ7pG').text
    return int(t_ads.replace('\xa0',''))

def get_total_pages(html):
    """WARN!!! повторяется логика !!!WARN
    возвращает количество страниц для последующего использования в цикле
    чтоб собрать объявления со всех страниц с объявлениями в категории.

    Спустя год я понял насколько этот код плох, строчные комменты для конкретики
    """
    soup = BSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a', \
        class_='pagination-page')[-1].get('href')
        # Предыдущий комент говорит о том, что возвращается string
    total_pages = pages.split('=')[1].split('&')[0]
    # Если string, то логично, но всё равно переделаю
    return int(total_pages)

def write_csv(data):
    """ Запись собранных файлов в файл """
    with open('avito_bikin_be.csv', \
        encoding="utf-8", mode="a") as parsed_data_file:
        writer = csv.writer(parsed_data_file)
        writer.writerow( (data['title'],
                          data['url'],
                          data['price'],
                          data['category'],
                          ) )

def get_page_data(html):
    """ Получение информации для построчной записи файл данных из объявления """
    soup = BSoup(html, 'lxml')

    #  ads - список объявлений
    #  Пошаговая логика:
    #  1) ищем родной блок каталог (тот что не является extra, с атрибутом "data-marker")
    #  2) ищем все ad
    #  3) записываем все ad в ads
    #
    #   type(ads) -> ResultSet
    #   type(ads[1]) -> tag
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




def main():
    """ Собранный скрипт для сбора информации """


    #url = 'https://www.avito.ru/bikin/bytovaya_elektronika'
    #url = 'https://www.avito.ru/moskva_i_mo/bytovaya_elektronika'
    url ='https://www.avito.ru/bikin/kvartiry/prodam/vtorichka-ASgBAgICAkSSA8YQ5geMUg'

    page_part = '?p='


    ads_in_url = total_ads(get_html(url))

    if ads_in_url <= 50:
        print(str(ads_in_url) + ' объявления, выгружаю...')
        get_page_data(get_html(url))
    else:
        print(str(ads_in_url) + ' предложений. Расчет страниц, прогружаю объявления...')
        total_pages = get_total_pages(get_html(url))
        for num_page in range(1, total_pages + 1):
            url_gen = url + page_part + str(num_page)
            html_qset = get_html(url_gen)
            get_page_data(html_qset)
            time.sleep(1)
    print("Вывод готов в текущей дериктории")


if __name__ == '__main__':
    main()
