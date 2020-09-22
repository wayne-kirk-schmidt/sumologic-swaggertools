#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provide high level document structure of the Sumo Logic sumologic-api.yaml
"""

import os
import re
import sys
import pprint
import time
from collections import defaultdict
from benedict import benedict
import requests

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

endpoint_dict = defaultdict(list)

if len(sys.argv) > 1:
    MY_OBJECT = sys.argv[1]
else:
    MY_OBJECT = 'all'

if len(sys.argv) > 2:
    MY_ACTION = sys.argv[2]
else:
    MY_ACTION = 'all'

for keypath in benedict.keypaths(yaml_dict):
    if re.match(r"paths\..*?\.(get|put|delete|post)$", keypath):
        pruned_path = keypath.replace('paths.', '')
        endpoint, method = pruned_path.rsplit('.', 1)
        endpoint_dict[endpoint].append(method)
        if MY_OBJECT in (endpoint, 'all'):
            if MY_ACTION  in (method, 'all'):
                print('{},{}'.format(endpoint, method))
