from .base import BaseTool
from agent.utils import retry
import requests
from typing import Dict,Tuple,Union
import os


class PayHistoryTool(BaseTool):
    name = "get_pay_history_api"
    is_remote=True
    description="这是一个充值记录查询工具"

    def __call__(self,*agrs, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api()
        return date_dict, code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self)->Union[Dict,None]:
        authCode = os.environ.get("authCode")
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/query/recharge"
        data = {
            "sdkAppKey": "zgydApp",
            "authCode": authCode
            }

        response = requests.post(post_url, json=data)

        if response.status_code == 200:
            result = response.json()['data']
            if not result:
                return {"result": "非常抱歉，未查到充值记录相关内容"}
            return result
        else:
            return {"result": "非常抱歉，网络异常，充值记录暂时无法查询"}



