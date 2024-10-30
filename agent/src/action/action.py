# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : action.py
# Time       ：2024/3/29 20:25
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from .base import BaseAction
from typing import Tuple
from utils import tool_dict
from agent.src.tool import BaseTool
from agent.utils import getMsgFromText
import json

class Action(BaseAction):
    def __init__(self,*args,**kwargs)->None:
        """
        :param tool_name:
        :param param_dict:
        :param args:
        :param kwargs:
        """
        super().__init__(*args,**kwargs)



    def check(self,tool:BaseTool,*args,**kwargs)->bool:
        """
        :param args:
        :param kwargs:
        :return:
        """
        try:
            if self.tool_name in tool_dict.keys():
                tool_valid=True
            else:
                tool_valid=False
        except:
            tool_valid=False

        if isinstance(self.param_dict,dict) and tool_valid:
            try:
                self.call_tool(tool,*args,**kwargs)
                return True
            except Exception as e:
                print(f"{self.param_dict} is not right,Error:{str(e)}")
                return False

    def call_tool(self, tool:BaseTool,*args, **kwargs):
        """
        :param tool:
        :param args:
        :param kwargs:
        :return:
        """
        tool.execute(self.tool_name, **self.param_dict)

    def is_finish(self,llm_output:str)->bool:
        ThoughtToken = "Thought"
        FinishToken = "Finish"
        if ThoughtToken in llm_output and FinishToken in llm_output:
            return True
        else:
            return False


    def parse(self,llm_output,*args,**kwargs)->Tuple:
        """
        :param args:
        :param kwargs:
        :return:
        """
        ActionToken="Action:"
        ParamToken="Action_Parameter:"
        llm_output = llm_output.replace("：", ":")

        tool_name = None
        param_dict = None
        if ActionToken in llm_output and ParamToken in llm_output:
            if not self.is_finish(llm_output):
                tool_name=getMsgFromText(llm_output,ActionToken,filter_token=True)
                param_dict=getMsgFromText(llm_output,ParamToken,filter_token=True)
        return tool_name,param_dict

    def get_api_param(self,llm_output):
        parse_res = self.parse(llm_output)
        tool_name = parse_res[0]
        param_dict = parse_res[-1]
        if isinstance(param_dict,str):
            try:
                param_dict=json.loads(param_dict)
            except:
                param_dict=eval(param_dict)
        self.tool_name=tool_name
        self.param_dict=param_dict
        return tool_name,param_dict






