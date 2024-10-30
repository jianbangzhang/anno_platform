# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base.py
# Time       ：2024/3/29 21:18
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from agent.src.action import Action
from agent.src.tool import BaseTool
from agent.src.prompt import PromptSingleChat
from agent.src.llm import AppLLM
from abc import ABC,abstractmethod

from agent.config import ToolConfig



class BaseAgent(ABC):
    def __init__(self,config:ToolConfig,tool:BaseTool,llm:AppLLM,action:Action,prompt_generator:PromptSingleChat,**kwargs):
        """
        :param config:
        :param tool:
        :param llm:
        :param action:
        :param prompt_generator:
        :param kwargs:
        """
        self.tool_config=config
        self.tool=tool
        self.action=action
        self.prompt_generator=prompt_generator
        self.kwargs=kwargs
        self.llm=llm

    @abstractmethod
    def _init(self,question:str):
        raise NotImplementedError


    @abstractmethod
    def singleChatRun(self,*args,**kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def multiChatRun(self,*args,**kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError
