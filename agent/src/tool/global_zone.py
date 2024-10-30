# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : global_zone.py
# Time       ：2024/5/7 10:15
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from .base import BaseTool
from agent.utils import retry
import requests
from typing import Dict,Tuple,Union
import os


class GlobalCommunicate(BaseTool):
    name = "global_connection_zone_api"
    is_remote=True
    description="这是一个全球通专区工具"

    def __call__(self, *args, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api()
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self)->Union[Dict,None]:
        authCode = os.environ.get("authCode")
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/globals/communicate"
        data = {
            "sdkAppKey": "zgydApp",
            "authCode": authCode,
            "phoneNumber": "17755161925"
        }

        response = requests.post(post_url, json=data)

        if response.status_code == 200:
            result = response.json()['data']
            if not result:
                return {"result": "非常抱歉，未查到全球通专区相关内容"}
            return result
        else:
            return {"result": "非常抱歉，网络异常，全球通专区暂时无法查询"}
