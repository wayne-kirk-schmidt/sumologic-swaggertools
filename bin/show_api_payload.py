#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Show documentation based on keypath of the sumologic-api.yaml file
"""

import re
import sys
import pprint
from benedict import benedict
import requests

__version__ = 1.00
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

API_URL = 'https://api.sumologic.com/docs/sumologic-api.yaml'
PP = pprint.PrettyPrinter(indent=4)

yaml_stream = requests.get(API_URL).text
yaml_dict = benedict.from_yaml(yaml_stream)

MY_TOPIC = sys.argv[1]

for keypath in benedict.keypaths(yaml_dict):
    if MY_TOPIC in keypath:
        path_base, path_end = keypath.rsplit('.', 1)
        if path_end in ('required', '$ref', 'example'):
            print('Keypath:\t{}'.format(keypath))
            my_dict = yaml_dict[keypath]
            PP.pprint(my_dict)
