from .base import BaseTool
from agent.utils import retry
import requests
from typing import Dict,Tuple,Union
import os



class SubServiceTool(BaseTool):
    name = "get_subscribe_service_api"
    is_remote=True
    description="这是一个已订业务查询工具"

    def __call__(self, *args, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api()
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self)->Union[Dict,None]:
        authCode = os.environ.get("authCode")
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/getSubscribeServiceApi"
        data = {
            "appKey": "zgydApp",
            "authCode": authCode,
        }


        response = requests.post(post_url, json=data)
        if response.status_code == 200:
            result = response.json()['data']
            if not result:
                return {"result": "非常抱歉，未查到已订业务相关内容"}
            return result
        else:
            return {"result": "非常抱歉，网络异常，已订业务暂时无法查询"}