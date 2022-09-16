#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2022/09/16 11:18:19
@Author  :   puffin jiang
@Version :   1.0
'''


import json
import string
from logging import getLogger
from random import choices

import setting as setting
from base_application import base_app
from models.link_mapping import LinkMapping
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from utils.common import generate_short_key_by_url, http_url_check, str_to_datetime

_logger = getLogger(__name__)


class BaseRequestHandle(SessionMixin, RequestHandler):
    pass


@base_app.route(r"/api/v1/shorten")
class ShortTen(BaseRequestHandle):

    async def post(self, *args):
        try:
            _logger.info(
                f"Received create short link from: {self.request.remote_ip}")
            params = json.loads(self.request.body)
            token = params.get("token")
            if not token or token.strip() != setting.SETTING.CHECK_TOKEN:
                _logger.warning(f"Failed to create short link due to "
                                f"wrong token: {token}")
                return self.write({'code': 401, 'message': u"身份验证失败"})
            url = params.get("url")
            if not url or not http_url_check(url):
                _logger.warning(f"Failed to create short link due to "
                                f"wrong url link: {url}")
                return self.write({"code": 400, "message": u"请检查链接是否正确"})
            url = url.strip()
            expire_time = params.get('expire_time')
            if expire_time:
                expire_time = str_to_datetime(expire_time)
            with self.make_session() as session:
                link_map = session.query(LinkMapping).filter(
                    LinkMapping.url == url).first()
                if not link_map:
                    link_map = LinkMapping(url=url)
                    # 获取key并更新到数据库
                    link_map.key = generate_link_mapping_key(url, session)
                    link_map.expire_time = expire_time
                    session.add(link_map)
                    session.commit()
                return self.write({
                    "code": 200,
                    "message": "SUCCESS",
                    "data": {
                        "key": link_map.key
                    }
                })
        except Exception as e:
            _logger.exception(f'Exception create short link mapping, '
                              f'params: {params}, error: {str(e)}')
            return self.write({"code": 500, "message": "请联系管理员"})


def generate_link_mapping_key(url, session):
    key = generate_short_key_by_url(url)
    # 检查是否有重复的key
    link_map = session.query(LinkMapping).filter_by(key=key).first()
    if not link_map:
        return key
    random_key = "".join(choices(string.ascii_letters + string.digits, k=7))
    url = "{}{}".format(url, random_key)
    return generate_link_mapping_key(url, session)


@base_app.route(r"/([^/]+)?")
class ShortLink(BaseRequestHandle):

    async def get(self, key, **kwargs):
        try:
            _logger.info(f"Received redirect short link "
                         f"from: {self.request.remote_ip}, key: {key}")
            with self.make_session() as session:
                link_map = session.query(LinkMapping).filter_by(
                    key=key).first()
                if link_map:
                    return self.redirect(link_map.url, status=302)
                return self.write({"code": 400, "message": "不存在的网页"})
        except AssertionError as e:
            _logger.exception(f"Exception redirect mapping url, "
                              f"key: {key}, error: {str(e)}")
            return self.write({"code": 500, "message": "请联系管理员！"})
