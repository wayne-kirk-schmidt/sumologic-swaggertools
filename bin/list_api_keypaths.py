#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shows the document structure for the Sumo Logic sumologic-api.yaml
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
    if 'info.version' in keypath:
        my_dict = yaml_dict[keypath]
        print('### API_Version: {}'.format(my_dict))
    if 'info.name' in keypath:
        my_dict = yaml_dict[keypath]
        print('### API_NAME: {}'.format(my_dict))
    print('{}'.format(keypath))
