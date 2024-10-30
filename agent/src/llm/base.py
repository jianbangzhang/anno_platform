# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base.py
# Time       ：2024/3/29 21:34
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from abc import ABC
from abc import abstractmethod


class LLM(ABC):
    def __init__(self,*args,**kwargs):
        pass

    @abstractmethod
    def chat(self,*args,**kwargs):
        raise NotImplementedError


    @abstractmethod
    def stream_chat(self,*args,**kwargs):
        raise NotImplementedError

    @abstractmethod
    def checkLLMOut(self,*args,**kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_stopWords(self,*args,**kwargs):
        pass
