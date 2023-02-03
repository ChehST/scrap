import time

import parser

def scrap_parse(url, **kwargs):
    """Собрал функцию  для парсинга"""

    PAGE_PART = '?p='
    html = parser.get_html(url,**kwargs)
    PARSED_DICT = parser.parse_dict(html)

    ads_in_url = PARSED_DICT["TOTAL_ADS"]

    if ads_in_url <= 50:
        print(str(ads_in_url) + ' объявления, выгружаю...')
        parser.get_page_data(html)
    else:
        print(str(ads_in_url) + ' предложений. Расчет страниц, прогружаю объявления...')
        total_pages = PARSED_DICT["TOTAL_PAGES"]
        for num_page in range(1, total_pages + 1):
            print("Смотрю страницу:",num_page)
            url_gen = url + PAGE_PART + str(num_page)

            html_qset = parser.get_html(url_gen,**kwargs)
            parser.get_page_data(html_qset)
            time.sleep(1)
    print("Вывод готов в текущей дериктории")