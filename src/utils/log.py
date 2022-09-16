#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   log.py
@Time    :   2022/09/16 11:19:39
@Author  :   puffin jiang
@Version :   1.0
'''

import logging
import os
from logging import config

import yaml


def init_log():
    filepath = os.path.join(os.getcwd(), 'logging.yml')
    with open(filepath, 'r', encoding='utf-8') as f:
        log_yaml = yaml.unsafe_load(f)
        log_dir = log_yaml.get('base_dir')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        config.dictConfig(config=log_yaml)
    logging.info(">>> init log file")
