#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provide high level document structure of the Sumo Logic sumologic-api.yaml
"""

import pprint
import requests
from benedict import benedict

__version__ = 1.00
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

API_URL = 'https://api.sumologic.com/docs/sumologic-api.yaml'
PP = pprint.PrettyPrinter(indent=2,width=40,depth=4)

yaml_stream = requests.get(API_URL).text
yaml_dict = benedict.from_yaml(yaml_stream)

for keypath in benedict.keypaths(yaml_dict):
    if '.put.parameters' in keypath:
        (_paths, endpoint, apimethod) = keypath.split('.')[:3]
        (_first, apiversion, objectname) = endpoint.split('/')[:3]
        print('API_ENDPOINT: {}'.format(endpoint))
        print('API_DETAILS: {} {} {}'.format(objectname, apimethod, apiversion))
        my_payload = dict()
        my_payload['api.version'] = apiversion
        my_payload[objectname] = dict()
        for my_item in yaml_dict[keypath]:
            my_key = my_item['name']
            is_required = 'False'
            if 'required' in my_item:
                is_required = my_item['required']
            my_payload[objectname][my_key] = is_required
        print('API_PAYLOAD: {}'.format(my_payload))
