from .base import BaseTool
from agent.utils import retry
import requests
from typing import Dict,Tuple,Union
import os


class FlowTool(BaseTool):
    name = "get_flow_info_api"
    is_remote=True
    description="这是一个流量查询工具"

    def __call__(self, *args, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api()
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self)->Union[Dict,None]:
        appKey = os.environ.get("appKey")
        authCode = os.environ.get("authCode")

        url = "http://172.31.205.27:32157/online-agent-tool/open/agent/getFlowInfoApi"
        data = {
            "authCode":authCode,
            "appKey":"zgydAppSDK"
        }

        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()['data']
            if not result:
                return {"result": "对不起，未查到流量相关内容"}
            return result
        else:
            return {"result": "对不起，网络异常，流量暂时无法查询"}