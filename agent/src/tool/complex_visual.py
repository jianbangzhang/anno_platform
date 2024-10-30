# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : complex_visual.py
# Time       ：2024/5/7 9:14
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""

from .base import BaseTool
from agent.utils import retry
from typing import Tuple




class ComplexVisualTool(BaseTool):
    name = "complex_visualization_api"
    is_remote=False
    description="这是一个画图工具"

    def __call__(self, *args, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api()
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self,*args,**kwargs):
        return {"result": "success"}