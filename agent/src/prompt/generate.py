# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : generate.py
# Time       ：2024/3/29 17:26
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from .base import BasePrompt
from typing import List
from utils import tool_dict
from agent.utils import question_format,available_tool_string
from agent.utils import get_tool_prompts
from data.parse_trajectory import parse_input_text


def get_normal_input(input):
    """
    :param input:
    :return:
    """
    result=[]
    if len(input)==0 or not any([True if t in input else False for t in ["Question","Thought","Action","Action_Parameter","Finish"]]):
        return result
    input=input.replace("<ret>","\n").replace("<end>","").strip()
    input_lst=[line.strip() for line in input.split("\n") if line.strip()]
    last_line=input_lst[-1]
    if last_line.startswith("Question") or last_line.startswith("Observation"):
        text_lst,code=parse_input_text(input_lst)
        if code==0:
            return text_lst
        return result
    else:
        return result

class PromptSingleChat(BasePrompt):
    prompt_type = "single_chat"
    prompt_description = "sys+tool+require+question+agent_trajectory"

    def __init__(self, system: str, require: str, *args, **kwargs):
        """
        :param system:
        :param require:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.system = system
        self.available_tool_string=available_tool_string
        self.require = require
        self.kwargs = kwargs


    def build_prompt(self, tool_list: List, question:str,history_lst: List, **kwargs):
        """
        :param tool_list:
        :param kwargs:
        :return:
        """
        history_lst=[e.strip() for e in history_lst]
        prompt = self.system+"\n"
        prompt += self.available_tool_string+"\n" + get_tool_prompts(tool_list,tool_dict)+"\n"
        prompt+= self.require+"".join(history_lst)
        return prompt.replace("\n","<ret>")

    def build_multi_prompt(self,tool_list: List, question:str,history_lst: List,current_chat_lst:List):
        """
        :param tool_list:
        :param question:
        :param history_lst:
        :param kwargs:
        :return:
        """
        history_lst=[e for lst in history_lst for e in lst]
        history_lst+= current_chat_lst
        history_lst = [e for e in history_lst if len(e)>0]
        prompt = self.system + "\n"
        prompt += self.available_tool_string + "\n" + get_tool_prompts(tool_list, tool_dict) + "\n"
        prompt += self.require+"".join(history_lst).strip()
        prompt += question_format(question)
        return prompt.replace("\n", "<ret>")

    def build_multi_prompt_next_call(self,tool_list: List,history_lst: List,current_chat_lst:List):
        """
        :param tool_list:
        :param question:
        :param history_lst:
        :param kwargs:
        :return:
        """
        history_lst=[e for lst in history_lst for e in lst]
        history_lst = [e for e in history_lst if len(e)>0]
        current_chat_lst= [e for e in current_chat_lst if len(e)>0]
        prompt = self.system + "\n"
        prompt += self.available_tool_string + "\n" + get_tool_prompts(tool_list, tool_dict) + "\n"
        prompt += self.require+"".join(history_lst).strip()+"".join(current_chat_lst).strip()
        return prompt.replace("\n", "<ret>")


    def init_prompt(self, tool_list: List,question:str,*args, **kwargs) -> str:
        """
        :param args:
        :param kwargs:
        :return:
        """
        init_prompt = self.system+"\n"
        init_prompt += self.available_tool_string + "\n" +get_tool_prompts(tool_list,tool_dict)+"\n"
        init_prompt += self.require+question_format(question)
        return init_prompt.replace("\n","<ret>")


    def build_prompt_for_call(self,input,tool_list):
        """
        :param input:
        :param tool_list:
        :return:
        """
        prompt = self.system + "\n"
        prompt += self.available_tool_string + "\n" + get_tool_prompts(tool_list, tool_dict) + "\n"
        input=input.replace("：",":").replace("<end><User>","Question").replace("<User>","Question").replace("<end><Bot>","").strip()
        input_lst=get_normal_input(input)
        prompt += self.require + "<end>".join(input_lst).strip()
        prompt=prompt.strip()
        if prompt.endswith("<Bot>") or prompt.endswith("<end>"):
            pass
        else:
            prompt+="<end>"
        return prompt.replace("\n", "<ret>")






class PromptMultiChat(BasePrompt):
    prompt_type = "single_chat"
    prompt_description = "sys+tool+require+question+agent_trajectory"

    def __init__(self, system: str, require: str, *args, **kwargs):
        super().__init__(*args,**kwargs)


    # ToDo