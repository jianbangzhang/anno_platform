from .base import BaseTool
from agent.utils import retry
import requests
from typing import Dict,Tuple,Union

class CalculatorTool(BaseTool):
    name = "calculator_api"
    is_remote=True
    description="这是一个计算器工具"

    def __call__(self, expression:str)->Tuple:
        date_dict,code=self._call_actual_api(expression)
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self, expression)->Union[Dict,None]:
        """
        :param expression:
        :return:
        """
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/calculator"
        data = {"expression": expression}
        response = requests.post(post_url, json=data)
        if response.status_code == 200:
            result = response.json()['data']
            if not result:
                return {"result": "非常抱歉，计算失败"}
            return result
        else:
            return {"result": "非常抱歉，网络异常，计算器工具暂时无法使用"}