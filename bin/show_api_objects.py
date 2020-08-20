#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shows all API endpoint paths in the Sumo Logic sumologic-api.yaml
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
    if re.match(r"paths\..*?\.(get|put|delete|post)$", keypath):
        keypath = keypath.replace('paths.', '')
        endpoint, method = keypath.rsplit('.', 1)
        endpoint_dict[endpoint].append(method)

for endpoint in endpoint_dict.keys():
    for method in endpoint_dict[endpoint]:
        print('{}'.format(endpoint))
