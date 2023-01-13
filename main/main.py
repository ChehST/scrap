import requests
from bs4 import BeautifulSoup as BSoup
import time
import csv


#  1) How many total ads n region?
#  2) How  many pages
#  3) Do a list with pages urls
#  4) collect data
#  5) get total pages, работает корректно если t_ads > 50!!!
#  6) додумать логику при t_ads < 50, когда есть extra


target_url = 'https://www.avito.ru/bikin/telefony'


# return url's html .text()
def get_html(url):
    r = requests.get(url)
    return r.text

# get catigories list
def get_cats(html):
    soup = BSoup(html, 'lxml')
    cats = soup.find_all('options')
    return cats

# return total ads in category
def total_ads(html):
    soup = BSoup(html, 'lxml')
    t_ads = soup.find('span', class_='page-title-count-wQ7pG').text
    return int(t_ads.replace('\xa0',''))

def get_total_pages(html):
    soup = BSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-root-Ntd_O').find_all('span',
                                                                 class_='pagination-item-JJq_j')[-1].get('href')
    # return result in string format
    total_pages = pages.split('=')[1].split('&')[0]

    return int(total_pages)

def write_csv(data):
    with open('avito_bikin_be.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow( (data['title'],
                          data['url'],
                          data['price'],
                          data['category'],
                          ) )

def get_page_data(html):
    soup = BSoup(html, 'lxml')

    #  ads - список объявлений
    #  Пошаговая логика:
    #  1) ищем родной блок каталог (тот что не является extra, с атрибутом "data-marker")
    #  2) ищем все ad
    #  3) записываем все ad в ads
    #
    #   type(ads) -> ResultSet
    #   type(ads[1]) -> tag
    ads = soup.find('div', class_='items-items-kAJAg', attrs={"data-marker": "catalog-serp"}).find_all('div', class_='iva-item-root-_lk9K')
    for ad in ads:
        # title,url, postday,
        try:
            title = ad.find('div', class_='iva-item-titleStep-pdebR').find('h3').text
        except:
            title = 'Null'

        try:
            url ='https://wwww.avito.ru' + ad.find('div', class_='iva-item-titleStep-pdebR').find('a').get('href')
        except:
            url = 'Null'

        try:
            price = ad.find('div', class_='iva-item-priceStep-uq2CQ').find('span', class_='price-text-_YGDY').text
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


    # url = 'https://www.avito.ru/bikin/telefony'
    # base_url = 'https://www.avito.ru/bikin/telefony?'
    url = 'https://www.avito.ru/bikin/bytovaya_elektronika'
    base_url = 'https://www.avito.ru/bikin/bytovaya_elektronika?'
    # url = 'https://www.avito.ru/moskva_i_mo/bytovaya_elektronika'
    # base_url = 'https://www.avito.ru/moskva_i_mo/bytovaya_elektronika?'

    page_part = 'p='


    ads_in_url = total_ads(get_html(url))

    if ads_in_url <= 50:
        print(str(ads_in_url) + ' объявления, выгружаю...')
        # debug code
    else:
        print(str(ads_in_url) + ' предложений. Расчет страниц, прогружаю объявления...')
        # debug code
        total_pages = get_total_pages(get_html(url))
        for num_page in range(1, total_pages + 1):
            url_gen = base_url + page_part + str(num_page)
            html_qset = get_html(url_gen)
            get_page_data(html_qset)
            time.sleep(1)



if __name__ == '__main__':
    main()

