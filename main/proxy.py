"""
:copyright: (c) 2022 by Sergey Cheh.
:license: Apache2, see LICENSE for more details.
"""

import pandas as pd


FILE_PATH = "proxie-list.csv"

def dict_proxies(file_name):
    """ Функция возвращает словарь с прокси
     """
    csv_pandas = pd.read_csv(file_name)
    proxy_dict = {}
    for column in csv_pandas.columns:
        # Вот тут мы сразу инициилизировали ключ и записали список всей колонки
        proxy_dict[column] = csv_pandas[column].tolist()

    return proxy_dict

proxies = dict_proxies(FILE_PATH)
