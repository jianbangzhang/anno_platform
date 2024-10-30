from .base import BaseTool
from agent.utils import retry
import requests
from typing import Dict,Tuple,Union

class KnowledgeTool(BaseTool):
    name = "knowledge_retrieval_api"
    is_remote=True
    description="这是一个知识库查询工具"

    def __call__(self, query, keyword, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api(query, keyword)
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self, query, keyword)->Union[Dict,None]:
        """
        :param query:
        :param keyword:
        :return:
        """
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/query/Knowledge"
        data = {
            "query": query,
            "keyword": keyword,
            "provinceCode": "250",
            "classification": "名词解释分类"
        }
        response = requests.post(post_url, json=data)
        if response.status_code == 200:
            result = response.json()['data']
            if not result:
                return {"result": f"非常抱歉，未在知识库查到{keyword}相关内容"}
            else:
                return result
        else:
            return {"result": "非常抱歉，网络异常，知识库暂时无法查询"}