# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : start_living.py
# Time       ：2024/5/7 10:08
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


class StartLivingTool(BaseTool):
    name = "start_living_expenses_info_api"
    is_remote=True
    description="这是一个打开生活缴费首页工具"

    def __call__(self, *args, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api()
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self)->Union[Dict,None]:
        authCode = os.environ.get("authCode")
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/lifePay/skip/index"
        data = {
            "sdkAppKey": "zgydApp",
            "authCode": authCode
        }

        response = requests.post(post_url, json=data)

        if response.status_code == 200:
            result = response.json()['data']
            if not result:
                return {"result": "非常抱歉，未查到生活缴费首页"}
            return result
        else:
            return {"result": "非常抱歉，网络异常，生活缴费首页工具暂时无法调用"}