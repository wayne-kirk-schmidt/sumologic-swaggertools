#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides list of Error Codes from the Sumo Logic sumologic-api.yaml
"""

import re
import pprint
from bs4 import BeautifulSoup
from benedict import benedict
import requests

__version__ = 1.00
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

API_URL = 'https://api.sumologic.com/docs/sumologic-api.yaml'
PP = pprint.PrettyPrinter(indent=4)

yaml_stream = requests.get(API_URL).text
yaml_dict = benedict.from_yaml(yaml_stream)

HTML_DATA = ""

PRINT_FLAG = 0
for keypath in benedict.keypaths(yaml_dict):
    if 'info.description' in keypath:
        my_dict = yaml_dict[keypath]
        for my_item in my_dict.split('\n'):
            if re.match(r".*?## Status Codes.*?", my_item):
                PRINT_FLAG = 1
            if re.match(r".*?## Filtering.*?", my_item):
                PRINT_FLAG = 0
            if PRINT_FLAG == 1:
                if not re.match(r".*?## Status Codes.*?", my_item):
                    my_item = re.sub('^.*?<table>', '<table>', my_item)
                    my_item = my_item.lstrip()
                    HTML_DATA = HTML_DATA + my_item

soup = BeautifulSoup(HTML_DATA, 'html.parser')
table_row_list = soup.find_all('tr')
for table_row in table_row_list:
    table_data_list = table_row.find_all('td')
    column_0 = table_data_list[0].text.lstrip().rstrip().replace(' ', '_')
    column_1 = table_data_list[1].text.lstrip().rstrip().replace(' ', '_')
    print(('{},{}').format(column_0, column_1))
