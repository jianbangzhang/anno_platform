# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : calendar.py
# Time       ：2024/3/29 15:06
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


class Calendar(BaseTool):
    name = "calendar_api"
    is_remote=True
    description="这是一个日历查询工具"

    def __call__(self, date:str, **kwargs)->Tuple:
        """
        :param date:
        :param kwargs:
        :return:
        """
        UsrArgs=kwargs
        # if UsrArgs:
        #     print(f"{UsrArgs} is not useful for this tool.")
        date_dict,code=self._call_remote_calendar(date)
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_remote_calendar(self,date:str)->Union[Dict,None]:
        """
        :param date:
        :return:
        """
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/query/date"
        data = {"date": date}

        response = requests.post(post_url, json=data)
        if response.status_code == 200:
            result = response.json()
            if not result:
                return {"result": "非常抱歉，未查到日历相关内容"}
            return result["data"]
        else:
            return {"result": "非常抱歉，网络异常，日历工具暂时无法使用"}

