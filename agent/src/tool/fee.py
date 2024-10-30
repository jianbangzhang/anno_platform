from .base import BaseTool
from agent.utils import retry
import requests
from typing import Dict,Tuple,Union
import os


class FeeTool(BaseTool):
    name = "get_fee_balance_api"
    is_remote=True
    description="这是一个话费查询工具"

    def __call__(self, *args, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api()
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self)->Union[Dict,None]:
        authCode = os.environ.get("authCode")
        get_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/fee"
        header = {
            "sdkAppKey": "zgydApp",
            "authCode": authCode
        }

        response = requests.get(get_url, headers=header)

        if response.status_code == 200:
            result = response.json()['data']
            if not result:
                return {"result": "非常抱歉，未查到话费相关内容"}
            return result
        else:
            return {"result": "非常抱歉，网络异常，话费暂时无法查询"}