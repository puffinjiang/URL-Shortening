#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2022/09/16 11:20:32
@Author  :   puffin jiang
@Version :   1.0
'''

import asyncio

from utils.common import load_config
from utils.log import init_log


async def main():
    # log and config must init before
    init_log()
    load_config()
    from base_application import base_app
    base_app.initialize()
    base_app.listen(9000)
    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(main())
    # res = random.sample(string.ascii_letters + string.digits, k=62)
    # print(f'res: {"".join(res)}')
