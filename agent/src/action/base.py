# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base.py
# Time       ：2024/3/29 20:17
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from abc import ABC
from abc import abstractmethod

class BaseAction(ABC):
    def __init__(self,*args,**kwargs):
        pass

    @abstractmethod
    def parse(self,*args,**kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def check(self,*args,**kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError


    @abstractmethod
    def call_tool(self,*args,**kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError
