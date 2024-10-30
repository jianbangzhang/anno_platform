# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : multimedia_content.py
# Time       ：2024/5/7 10:14
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


class MultimediaContentTool(BaseTool):
    name = "multimedia_content_search_api"
    is_remote=True
    description="这是一个影视、音乐、阅读内容查询工具"

    def __call__(self, user_query,moduleType,keyword, *args, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api(user_query,moduleType,keyword)
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self,user_query,moduleType,keyword)->Union[Dict,None]:
        authCode = os.environ.get("authCode")
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/multimedia/content"
        data = {
            "sdkAppKey": "zgydApp",
            "authCode": authCode,
            "user_query":user_query,
            "moduleType":moduleType,
            "keyword":keyword
        }

        response = requests.post(post_url, json=data)

        if response.status_code == 200:
            result = response.json()['data']
            if not result:
                return {"result": "非常抱歉，未查到影视、音乐、阅读相关内容"}
            return result
        else:
            return {"result": "非常抱歉，网络异常，影视、音乐、阅读内容暂时无法查询"}

