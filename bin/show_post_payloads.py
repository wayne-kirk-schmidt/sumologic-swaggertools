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
PP = pprint.PrettyPrinter(indent=4)

yaml_stream = requests.get(API_URL).text
yaml_dict = benedict.from_yaml(yaml_stream)

for keypath in benedict.keypaths(yaml_dict):
    if 'post.requestBody.content.application/json.schema.$ref' in keypath:
        if '{' not in keypath:
            (_paths, endpoint, method) = keypath.split('.')[:3]
            (_first, apiversion, objectname) = endpoint.split('/')[:3]
            print('{} {} {} {}'.format(endpoint, method, apiversion, objectname))
            keypayload = yaml_dict[keypath]
            keypayload = keypayload.replace('#/', '')
            keypayload = keypayload.replace('/', '.')
            my_payload = dict()
            my_payload['api.version'] = apiversion
            my_payload[objectname] = dict()
            if 'properties' in yaml_dict[keypayload]:
                ### PP.pprint(yaml_dict[keypayload]['properties'])
                for ATTRIBUTE in yaml_dict[keypayload]['properties']:
                    my_payload[objectname][ATTRIBUTE] = 'example_field'
                    for item in yaml_dict[keypayload]['properties'].items():
                        ATTRIBUTE = str(item[0])
                        if 'example' in item[1].keys():
                            my_value = item[1]['example']
                            my_payload[objectname][ATTRIBUTE] = my_value
                PP.pprint(my_payload)
            elif 'allOf' in yaml_dict[keypayload]:
                for my_item in yaml_dict[keypayload]['allOf']:
                    if '$ref' in my_item:
                        refpath = my_item['$ref']
                        refpath = refpath.replace('#/', '')
                        refpath = refpath.replace('/', '.')
                        if 'properties' in yaml_dict[refpath]:
                            for ATTRIBUTE in yaml_dict[refpath]['properties']:
                                my_payload[objectname][ATTRIBUTE] = 'example_field'
                                for item in yaml_dict[refpath]['properties'].items():
                                    ATTRIBUTE = str(item[0])
                                    if 'example' in item[1].keys():
                                        my_value = item[1]['example']
                                        my_payload[objectname][ATTRIBUTE] = my_value
                    if 'properties' in my_item:
                        for ATTRIBUTE in my_item['properties']:
                            print(ATTRIBUTE)
                            my_payload[objectname][ATTRIBUTE] = 'example_field'
                            for item in my_item['properties'].items():
                                ATTRIBUTE = str(item[0])
                                if 'example' in item[1].keys():
                                    my_value = item[1]['example']
                                    my_payload[objectname][ATTRIBUTE] = my_value
                PP.pprint(my_payload)
