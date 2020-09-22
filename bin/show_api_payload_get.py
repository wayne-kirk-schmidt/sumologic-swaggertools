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
    if '.get.parameters' in keypath:
        (_paths, endpoint, apimethod) = keypath.split('.')[:3]
        (_first, apiversion, objectname) = endpoint.split('/')[:3]
        print('API_ENDPOINT: {}'.format(endpoint))
        print('API_DETAILS: {} {} {}'.format(objectname, apimethod, apiversion))
        my_payload = dict()
        my_payload['api.version'] = apiversion
        my_payload[objectname] = dict()
        for my_item in yaml_dict[keypath]:
            my_key = my_item['name']
            IS_REQUIRED = 'False'
            if 'required' in my_item:
                IS_REQUIRED = my_item['required']
            my_payload[objectname][my_key] = IS_REQUIRED
        print('API_PAYLOAD: {}'.format(my_payload))
