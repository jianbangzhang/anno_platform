# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : message.py
# Time       ：2024/3/29 16:36
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
import json
from agent.utils import question_format



class BaseMessage(object):
    def __init__(self,*args,**kwargs):
        raise NotImplementedError

    @classmethod
    def wrapper(cls,*args,**kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError


class QuestionMessage(BaseMessage):
    @classmethod
    def wrapper(cls,question:str,**kwargs):
        """
        :param question:
        :param kwargs:
        :return:
        """
        question=question_format(question)
        return question


class ObservationMessage(BaseMessage):
    @classmethod
    def wrapper(cls,Observation_dict:str,**kwargs)->str:
        """
        :param Observation_dict:
        :param kwargs:
        :return:
        """
        is_json_string=kwargs.get("json_string",False)
        if is_json_string:
            observation_format = f"Observation: {json.dumps(Observation_dict)}<end>"
        else:
            observation_format=f"Observation: {Observation_dict}<end>"
        return observation_format









