#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   base_application.py
@Time    :   2022/09/16 11:21:22
@Author  :   puffin jiang
@Version :   1.0
'''

from logging import getLogger

import tornado.web

from utils.common import load_module
from utils.database import create_table, db

_logger = getLogger(__name__)


class BaseApplication(tornado.web.Application):

    def route(self, pattern):

        def _(handler):
            handler_pattern = [(pattern, handler)]
            self.add_handlers(".*$", handler_pattern)
            return handler

        return _

    def register_api(self, module_name):
        load_module(module_name)

    def initialize(self):
        self.register_api('api')
        create_table()


base_app = BaseApplication(db=db)
base_app.initialize()
