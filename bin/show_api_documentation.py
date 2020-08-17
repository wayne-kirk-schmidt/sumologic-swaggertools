#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides documentation of select areas of the Sumo Logic sumologic-api.yaml
"""

import sys
import pprint
from collections import defaultdict
from benedict import benedict
import requests

if len(sys.argv) <= 1:
    print('usage: show_api_documentation.py <object> <topic>')
    sys.exit(1)

if len(sys.argv) > 1:
    MY_OBJECT = sys.argv[1]

if len(sys.argv) > 2:
    MY_TOPIC = sys.argv[2]
else:
    MY_TOPIC = 'all'

__version__ = 1.00
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

API_URL = 'https://api.sumologic.com/docs/sumologic-api.yaml'
PP = pprint.PrettyPrinter(indent=4)

yaml_stream = requests.get(API_URL).text
yaml_dict = benedict.from_yaml(yaml_stream)

endpoint_dict = defaultdict(list)

for keypath in benedict.keypaths(yaml_dict):
    if MY_OBJECT in keypath:
        if MY_TOPIC in (keypath, 'all'):
            print('Keypath: {}'.format(keypath))
            if keypath in yaml_dict:
                my_dict = yaml_dict[keypath]
                PP.pprint(my_dict)
