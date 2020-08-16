#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provide the version and title of the Sumo Logic API sumologic-api.yaml
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

my_title = yaml_dict['info.title']
print('API_Name|{}'.format(my_title))

my_version = yaml_dict['info.version']
print('API_Version|{}'.format(my_version))
