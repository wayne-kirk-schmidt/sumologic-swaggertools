#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List all API servers and deployments within the Sumo Logic sumologic-api.yaml
"""

import re
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
    if re.match(r"servers$", keypath):
        for server_dict in yaml_dict[keypath]:
            mydict = server_dict
            my_url = mydict['url'].replace("'", "")
            my_deployment = mydict['description'].split(" ")[0]
            print('{},{}'.format(my_deployment, my_url))
