#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   common.py
@Time    :   2022/09/16 11:19:13
@Author  :   puffin jiang
@Version :   1.0
'''

import importlib
import logging
import os
import re
from datetime import datetime

import mmh3
import yaml
from setting import SETTING

_logger = logging.getLogger(__name__)


def load_config():
    try:
        filepath = os.path.join(os.getcwd(), 'config.yml')
        with open(filepath, "r", encoding='utf-8') as f:
            config_yaml = yaml.safe_load(f)
        result = parse_config_yaml(config_yaml)
        for key, value in result.items():
            setattr(SETTING, key.upper(), value)
        _logger.info('>>> init load config')
        return result
    except Exception as e:
        _logger.exception(f">>> Error load config, error: {str(e)}")
    return {}


def parse_config_yaml(config_yaml: dict, result=None):
    if result is None:
        result = {}
    for key, value in config_yaml.items():
        if isinstance(value, dict):
            parse_config_yaml(value, result=result)
        else:
            result[key] = value
    return result


def http_url_check(url):
    """
        校验url是否合法，只允许http和https开头的url
    :param url:
    :return:
    """
    regex = re.compile(
        r'^(?:http)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE)
    return re.match(regex, url.strip())


def base62_encode(number, alphabet):
    """
        encode number to str code
    Args:
        number: number need to encode
        alphabet: base str

    Returns:

    """
    arr = []
    if number < 0:
        number = abs(number)
    base = len(alphabet)
    while number:
        number, rem = divmod(number, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def generate_short_key_by_url(url):
    return base62_encode(mmh3.hash(url), SETTING.BASE62_STR)


def load_module(module_name):
    """
        register api module
    :param module_name: module name need to load
    :return:
    """
    importlib.import_module(module_name)


def str_to_datetime(date_str, format="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(date_str, format)
