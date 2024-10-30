# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : global_connection.py
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


class GlobalTravalTool(BaseTool):
    name = "global_connection_traval_api"
    is_remote=True
    description="这是一个全球通出行工具"

    def __call__(self, city,travel_type,*args, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api(city,travel_type)
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self,city,travel_type)->Union[Dict,None]:
        authCode = os.environ.get("authCode")
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/globals/travel"
        # data = {
        #     'sdkAppKey': 'zgydApp',
        #     'authCode': authCode,
        #     'phoneNumber': '17755161925',
        #     'globalTravelItem': {
        #         'city': city,
        #         'travel_type': travel_type,
        #     }
        # }
        data={
              "phoneNumber": "17755161925",
              "provinceCode": "551",
              "globalTravelItem": {
                "citys": city,
                "travel_type": travel_type,
                "city": "北京",
                "appVersion": "10.0.0"
              }
            }

        response = requests.post(post_url, json=data)

        if response.status_code == 200:
            result = response.json()['data']
            if not result:
                return {"result": "非常抱歉，未查到全球通出行相关内容"}
            return result
        else:
            return {"result": "非常抱歉，网络异常，全球通出行暂时无法调用"}