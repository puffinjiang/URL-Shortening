#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   database.py
@Time    :   2022/09/16 11:19:25
@Author  :   puffin jiang
@Version :   1.0
'''

from setting import SETTING
from tornado_sqlalchemy import SQLAlchemy

db = SQLAlchemy(url=SETTING.SQLALCHEMY_DATABASE_URI)


def create_table():
    """
        create all tables by model， module must be load to create all tables from model
    Args:
        database (SQLAlchemy): the db
    """
    from utils.common import load_module
    load_module('models')
    db.metadata.create_all(bind=db.engine)
