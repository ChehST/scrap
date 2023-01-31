# AUTHOR: github.com/ChehST


import argparse

from ScrapParser import scrap_parse
from proxy import dict_proxies


parser = argparse.ArgumentParser(description="Управление парсером Scrap")
parser.add_argument('target_url', type=str, help="Clipboard url with https://")
parser.add_argument('-p', '--proxy', type=str, help='Путь до файла с прокси')
args = parser.parse_args()

if args.proxy:
    PROXIES = dict_proxies(args.proxy)

scrap_parse(args.target_url, proxies=PROXIES)
