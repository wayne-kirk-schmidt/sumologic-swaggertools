#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides detailed Payload information from a Sumo Logic a sumologic-api.yaml
"""

import re
import sys
import pprint
from collections import defaultdict
from benedict import benedict
import requests

if len(sys.argv) > 1:
    MY_OBJECT = sys.argv[1]
else:
    MY_OBJECT = 'all'

if len(sys.argv) > 2:
    MY_ACTION = sys.argv[2]
else:
    MY_ACTION = 'all'

__version__ = 1.00
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

API_URL = 'https://api.sumologic.com/docs/sumologic-api.yaml'
PP = pprint.PrettyPrinter(indent=4)

yaml_stream = requests.get(API_URL).text
yaml_dict = benedict.from_yaml(yaml_stream)

endpoint_dict = defaultdict(list)

for keypath in benedict.keypaths(yaml_dict):
    if re.match(r"paths\..*?\.(get|put|delete|post)$", keypath):
        pruned_path = keypath.replace('paths.', '')
        endpoint, method = pruned_path.rsplit('.', 1)
        payload = dict()
        if MY_OBJECT in (endpoint, 'all'):
            if MY_ACTION in (method, 'all'):
                if 'parameters' in yaml_dict[keypath]:
                    param_dict = yaml_dict[keypath]['parameters']
                    for list_elem in param_dict:
                        if 'name' in list_elem:
                            my_key = list_elem['name']
                        if 'required' in list_elem:
                            my_value = list_elem['required']
                            if str(my_value) == 'True':
                               my_status = 'required'
                            else:
                               my_status = 'optional'
                        payload[my_key] = my_status
                elif 'requestBody' in yaml_dict[keypath]:
                    payload = yaml_dict[keypath]['requestBody']['content']['application/json']['schema']
                else:
                    payload = 'no_payload_needed'
                print('{},{},{}'.format(endpoint, method, payload))
