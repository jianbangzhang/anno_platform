from .base import BaseTool
from agent.utils import retry
import requests
from typing import Dict,Tuple,Union,List
import os
import json

class BillCost(BaseTool):
    name = "get_bill_cost_in_month_api"
    is_remote=True
    description="这是一个账单查询工具"

    def __call__(self, year_month:str, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api(year_month)
        return date_dict,code


    @retry(max_retry=1, delay=0)
    def _call_actual_api(self, year_month):
        """
        :param year_month:
        :return:
        """
        appKey= os.environ.get("appKey")
        authCode=os.environ.get("authCode")
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/getBillCostInMonthApi"
        data = {
                "appKey": "zgydAppSDK",
                "authCode": authCode,
                "year_month": year_month,
            }

        response = requests.post(post_url, json=data)

        if response.status_code == 200:
            result = response.json()["data"]
            if not result:
                return {"result": "非常抱歉，未查到账单相关内容"}
            return result
        else:
            return {"result": "非常抱歉，网络异常，账单暂时无法查询"}