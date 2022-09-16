#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   setting.py
@Time    :   2022/09/16 11:21:52
@Author  :   puffin jiang
@Version :   1.0
'''


class Setting(object):
    """
    This is a configuration file
    Args:
        object (_type_): _description_
    """
    SQLALCHEMY_DATABASE_URI = None
    CHECK_TOKEN = None


SETTING = Setting()
