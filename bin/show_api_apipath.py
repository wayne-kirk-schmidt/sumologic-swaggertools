#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provide high level document structure of the Sumo Logic sumologic-api.yaml
"""

import os
import pprint
import time
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

for keypath in benedict.keypaths(yaml_dict):
    print('{}'.format(keypath))
