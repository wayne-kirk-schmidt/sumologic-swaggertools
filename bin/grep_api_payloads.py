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

if len(sys.argv) <= 1:
    print('usage: grep_api_payloads.py <object> <action>')
    sys.exit(1)

if len(sys.argv) > 1:
    MY_OBJECT = sys.argv[1]

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
        endpoint_dict[endpoint].append(method)
        if MY_OBJECT in endpoint:
            if MY_ACTION in (method, 'all'):
                print('{}|{}'.format(endpoint, method))
                PP.pprint(yaml_dict[keypath])
