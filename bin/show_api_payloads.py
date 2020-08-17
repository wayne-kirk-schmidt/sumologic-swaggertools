#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shows payloads required for all API endpoints in the Sumo Logic sumologic-api.yaml
"""

import re
import pprint
from collections import defaultdict
from benedict import benedict
import requests

__version__ = 1.00
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

API_URL = 'https://api.sumologic.com/docs/sumologic-api.yaml'
PP = pprint.PrettyPrinter(indent=4)

yaml_stream = requests.get(API_URL).text
yaml_dict = benedict.from_yaml(yaml_stream)

endpoint_dict = defaultdict(list)

for keypath in benedict.keypaths(yaml_dict):
    if re.match(r"paths\..*?\.(put|get|delete|post)$", keypath):
        pruned_path = keypath.replace('paths.', '')
        endpoint, method = pruned_path.rsplit('.', 1)
        if 'parameters' in yaml_dict[keypath]:
            MY_DICT = dict()
            for yaml_dict_item in yaml_dict[keypath]['parameters']:
                my_key = yaml_dict_item['name']
                if 'required' in yaml_dict_item:
                    MY_VALUE = yaml_dict_item['required']
                    if MY_VALUE:
                        MY_VALUE = 'required'
                    else:
                        MY_VALUE = 'optional'
                else:
                    MY_VALUE = 'undefined'
                MY_DICT[my_key] = MY_VALUE
        elif 'requestBody' in yaml_dict[keypath]:
            MY_DICT = yaml_dict[keypath]['requestBody']['content']
            ### ['content']['application/json']['schema']
        else:
            if method == 'get':
                MY_DICT = 'GET-unnecessary'
            elif method == 'post':
                MY_DICT = 'POST-unnecessary'
            else:
                MY_DICT = yaml_dict[keypath]
        print('{}|{}|{}'.format(endpoint, method, MY_DICT))
