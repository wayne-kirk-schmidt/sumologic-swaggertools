#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provide high level document structure of the Sumo Logic sumologic-api.yaml
"""

import os
import pprint
import time
import re
from bs4 import BeautifulSoup
import requests
from benedict import benedict

__version__ = 1.00
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

API_URL = 'https://api.sumologic.com/docs/sumologic-api.yaml'
API_FILE = '/var/tmp/sumologic-api.yaml'
PP = pprint.PrettyPrinter(indent=2, width=40, depth=4)

SEC2MIN = 60
MIN2HOURS = 60
NUM_HOURS = 4

TIME_LIMIT = SEC2MIN * MIN2HOURS * NUM_HOURS

if os.path.exists(API_FILE):
    stat_time = os.path.getctime(API_FILE)
    time_now = time.time()
    time_delta = (time_now - stat_time)
    if int(time_delta) > TIME_LIMIT:
        yaml_stream = requests.get(API_URL).text
        with open(API_FILE, 'w') as file_object:
            file_object.write(yaml_stream)
else:
    yaml_stream = requests.get(API_URL).text
    with open(API_FILE, 'w') as file_object:
        file_object.write(yaml_stream)

yaml_dict = benedict.from_yaml(API_FILE)

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
