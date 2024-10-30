# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : llm.py
# Time       ：2024/3/29 21:34
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""

from .base import LLM
from agent.utils import call_remote_agent
from agent.utils import checkOutput

class AppLLM(LLM):
    def __init__(self,*args,**kwargs):
        super(AppLLM, self).__init__(*args,**kwargs)
        self.endTokenList=["Observation","Observation:","Observation：","Observation\n"]

    def chat(self,prompt, is_remote,*args, **kwargs):
        """
        :param prompt:
        :param is_remote:
        :param args:
        :param kwargs:
        :return:
        """
        if is_remote:
            response=call_remote_agent(prompt)

            for stopWords in self.endTokenList:
                if stopWords in str(response):
                    stop_pos=response.index(stopWords)
                    response=response[:stop_pos]
            return response
        else:
            #ToDo
            pass

    def stream_chat(self,prompt,is_remote=True, *args, **kwargs):
        if is_remote:
            from websockets.sync.client import connect
            import json

            # auth_url="ws://172.29.100.69:9979/turing/v3/gpt" #华为
            auth_url="ws://36.138.59.240:9999/turing/v3/gpt" # a100

            prompt_dict={
                "header": {
                    "traceId": "SPARK_DEMO"
                },
                "parameter": {
                    "chat": {
                        "temperature": 0,
                        "max_tokens": 4096,
                        "top_k": 1
                    }
                },
                "payload": {
                    "message": {
                        "text": [
                            {"role": "user","content":prompt}
                        ]
                    }
                }
            }

            message = json.dumps(prompt_dict, ensure_ascii=False)
            with connect(auth_url) as ws:
                response = ""
                ws.send(message)
                for re in ws:
                    result = json.loads(re)
                    try:
                        response += result["payload"]["choices"]["text"][0]["content"]
                        response = response.replace("<ret>", "\n")
                    except Exception as e:
                        return e

            for stopWords in self.endTokenList:
                if stopWords in response:
                    stop_pos = response.index(stopWords)
                    response = response[:stop_pos]
            yield response
        else:
            # ToDo
            pass


    def checkLLMOut(self, llm_out):
        """
        :param llm_out:
        :return:
        """
        FinishFormat=["Thought","Finish"]
        SubProcessFormat=["Thought","Action","Action_Parameter"]
        is_finish=checkOutput(llm_out,FinishFormat)
        is_subprocess=checkOutput(llm_out,SubProcessFormat)
        is_valid=is_subprocess or is_finish
        is_stop=is_finish
        return is_valid,is_stop


    def add_stopWords(self,token=None,*args,**kwargs):
        """
        :param token: end token not in EndTokenList
        :return:
        """
        if token is not None and token not in self.endTokenList:
            self.endTokenList.append(token)
        else:
            pass




