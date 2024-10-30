# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : points_info.py
# Time       ：2024/4/2 13:16
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



class PointsInfoTool(BaseTool):
    name = "points_info_api"
    is_remote=True
    description="这是一个积分查询工具"

    def __call__(self, *args, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api()
        return date_dict,code


    @retry(max_retry=1, delay=0)
    def _call_actual_api(self):
        """
        :param date:
        :return:
        """
        authCode = os.environ.get("authCode")
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/pointsInfoApi"
        data = {
            "sdkAppKey": "zgydAppSDK",
            "appKey": "zgydApp",
            "authCode": authCode,
        }


        response = requests.post(post_url, json=data)
        if response.status_code == 200:
            result = response.json()['data']
            if not result:
                return {"result": "非常抱歉，未查到积分的相关内容"}
            return result
        else:
            return {"result": "非常抱歉，网络异常，积分暂时无法查询"}
