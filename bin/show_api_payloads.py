#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides Payload summary information for the Sumo Logic sumologic-api.yaml
"""

import re
import pprint
from benedict import benedict
import requests

__version__ = 1.00
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

API_URL = 'https://api.sumologic.com/docs/sumologic-api.yaml'

PP = pprint.PrettyPrinter(indent=4)

yaml_stream = requests.get(API_URL).text
yaml_dict = benedict.from_yaml(yaml_stream)

def get_parameters(target_dict):
    """
    Extract out key value pairs
    """
    my_payload = dict()
    for list_elem in target_dict:
        if 'name' in list_elem:
            my_key = list_elem['name']
            if 'required' in list_elem:
                my_value = list_elem['required']
                if str(my_value) == 'True':
                    my_status = 'required'
                else:
                    my_status = 'optional'
                my_payload[my_key] = my_status
    return my_payload

def resolve_corner_cases(target_dict):
    """
    Address any remaining corner cases
    """
    my_payload = target_dict
    if method in 'get':
        my_payload = {'payload' : 'unnecessary'}
    if method in 'post':
        _my_payload = target_dict['requestBody']
        my_payload = _my_payload['content']['application/json']['schema']

    return my_payload

def get_requestbody(target_dict):
    """
    Parse out payload based requestbody data structure
    """
    my_payload = target_dict['content']['application/json']['schema']
    return my_payload

def get_by_post_method(target_dict):
    """
    Resolve post method payloads
    """
    try:
        _my_payload = target_dict['requestBody']
        my_payload = _my_payload['content']['application/json']['schema']
    except:
        my_payload = target_dict
    if 'responses' in target_dict:
        my_payload = {'payload' : 'unnecessary'}

    return my_payload

def determine_payload(target_dict):
    """
    Parse out payload based on method, data from yaml file
    """
    my_payload = dict()

    if 'parameters' in target_dict:
        my_payload = get_parameters(target_dict['parameters'])
    elif 'requestBody' in target_dict:
        my_payload = get_requestbody(target_dict['requestBody'])
    elif method == 'post':
        my_payload = get_by_post_method(target_dict)
    elif method == 'delete':
        my_payload = target_dict

    if len(my_payload) == 0:
        my_payload = resolve_corner_cases(target_dict)

    return my_payload

for keypath in benedict.keypaths(yaml_dict):
    if re.match(r"paths\..*?\.(get|put|delete|post)$", keypath):
        pruned_path = keypath.replace('paths.', '')
        endpoint, method = pruned_path.rsplit('.', 1)
        MY_PAYLOAD = determine_payload(yaml_dict[keypath])
        print('{},{},{}'.format(endpoint, method, MY_PAYLOAD))
