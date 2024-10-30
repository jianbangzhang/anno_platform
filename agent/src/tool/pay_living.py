# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : pay_living.py
# Time       ：2024/5/7 9:58
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


class PayLivingTool(BaseTool):
    name = "pay_living_expenses_api"
    is_remote=True
    description="这是一个生活缴费充值工具"

    def __call__(self, type,amount,*args, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api(type,amount)
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self,type,amount)->Union[Dict,None]:
        authCode = os.environ.get("authCode")
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/lifePay/recharge"
        data = {
            "sdkAppKey": "zgydApp",
            "authCode": authCode,
            "type":type,
            "amount":amount

        }

        response = requests.post(post_url, json=data)

        if response.status_code == 200:
            result = response.json()['data']
            print(result)
            if not result:
                return {"result": "非常抱歉，未查到生活缴费余额充值"}
            return result
        else:
            return {"result": "非常抱歉，网络异常，生活缴费余额充值暂时无法调用"}