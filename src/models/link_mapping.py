#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   link_mapping.py
@Time    :   2022/09/16 11:18:48
@Author  :   puffin jiang
@Version :   1.0
'''

from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, Integer, String
from utils.database import db


def get_datetime_of_next_year(days=365):
    return datetime.now() + timedelta(days=days)


class LinkMapping(db.Model):
    """
    Extend sqlalchemy modle. A model of link mappings
    Args:
        db (_type_): _description_

    Returns:
        _type_: _description_
    """
    __tablename__ = 'link_mappings'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    url = Column(String, unique=True)
    create_time = Column(DateTime, default=datetime.now)
    expire_time = Column(DateTime, default=get_datetime_of_next_year)

    def __repr__(self):
        return '<id {}>'.format(self.id)
