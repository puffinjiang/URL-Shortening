#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   test_short_link.py
@Time    :   2022/09/16 11:22:21
@Author  :   puffin jiang
@Version :   1.0
'''

import json
import logging
from datetime import datetime

import setting
from tornado.escape import json_encode
from tornado.testing import AsyncHTTPTestCase

_logger = logging.getLogger(__name__)


class TestShortLink(AsyncHTTPTestCase):

    def get_app(self):
        from utils.common import load_config
        from utils.log import init_log
        init_log()
        load_config()
        from base_application import base_app
        base_app.initialize()
        return base_app

    def get_url_by_key(self, code):
        # this response  is the direct result, so the code is 200, but not 302
        response = self.fetch(f'/{code}')
        self.assertEqual(response.code, 200)

    def create_shorten(self, params):
        response = self.fetch("/api/v1/shorten",
                              method="POST",
                              body=json_encode(params))
        assert response.code == 200
        result = json.loads(response.body)
        self.assertEqual(result.get("message"), "SUCCESS")
        return result

    def test_create_and_get(self):
        params = {
            "token": setting.SETTING.CHECK_TOKEN,
            "url": "https://www.baidu.com"
        }
        create_data = self.create_shorten(params)
        code = create_data.get("data").get("key")
        _logger.info(f"get result short key: {code}")
        self.get_url_by_key(code)

    def test_create_generate_link_map_key(self):
        params = {
            "token": setting.SETTING.CHECK_TOKEN,
            "url": "https://www.baidu.com"
        }
        result = self.create_shorten(params)
        from sqlalchemy.orm import sessionmaker
        from utils.database import db
        session = sessionmaker(db.engine)()
        with session as session:
            from api.main import generate_link_mapping_key
            key = generate_link_mapping_key(params['url'], session)
            self.assertNotEqual(result.get("data").get("key"), key)

    def test_str_to_datetime(self):
        date_str = "2022-09-05 13:43:30"
        from utils.common import str_to_datetime
        data = str_to_datetime(date_str)
        self.assertEqual(datetime(2022, 9, 5, 13, 43, 30), data)
