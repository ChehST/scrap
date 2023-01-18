# AUTHOR: github.com/ChehST


import argparse

from ScrapParser import scrap_parse

parser = argparse.ArgumentParser(description="Управление парсером Scrap")
parser.add_argument('target_url', type=str, help="Clipboard url with https://")
args = parser.parse_args()

scrap_parse(args.target_url)
