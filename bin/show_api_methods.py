#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provide high level document structure of the Sumo Logic sumologic-api.yaml
"""

import os
import re
import time
import yaml
import ruamel.yaml
import requests

__version__ = 1.00
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

API_URL = 'https://api.sumologic.com/docs/sumologic-api.yaml'
API_FILE = '/var/tmp/sumologic-api.yaml'

TIME_LIMIT = 4 * 60 * 60

if os.path.exists(API_FILE):
    stat_time = os.path.getctime(API_FILE)
    time_now = time.time()
    time_delta = (time_now - stat_time)
    if int(time_delta) > TIME_LIMIT:
        yaml_stream = requests.get(API_URL).text
        with open(API_FILE, 'w') as file_object:
            file_object.write(yaml_stream)
else:
    yaml_stream = requests.get(API_URL).text
    with open(API_FILE, 'w') as file_object:
        file_object.write(yaml_stream)

def pathify(dictionary, mypath=None, paths=None, joinchar='.'):
    """
    Recursively parse paths in the YAML file and join them with a common separator
    """
    if mypath is None:
        paths = {}
        pathify(dictionary, "", paths, joinchar=joinchar)
        return paths
    pathname = mypath
    if mypath != "":
        pathname += '.'
    if isinstance(dictionary, dict):
        for key in dictionary:
            value = dictionary[key]
            pathify(value, pathname + key, paths, joinchar=joinchar)
    elif isinstance(dictionary, list):
        for index, entry in enumerate(dictionary):
            pathify(entry, pathname + str(index), paths, joinchar=joinchar)
    else:
        paths[mypath] = dictionary
    return paths

yaml = ruamel.yaml.YAML(typ='safe')

with open(API_FILE, "r") as yaml_stream:
    pathsdict = pathify(yaml.load(yaml_stream))

for path_key, path_value in pathsdict.items():
    if re.match(r"paths.*.tags.0", path_key):
        path_key = path_key.replace("paths.","")
        path_key = path_key.replace(".tags.0","")
        apipath, method = path_key.split(".")
        print('{},{},{}'.format(path_value, apipath, method))
