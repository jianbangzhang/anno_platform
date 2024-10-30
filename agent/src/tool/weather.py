# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : weather.py
# Time       ：2024/3/29 15:04
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from .base import BaseTool
from agent.utils import retry

from typing import List,Tuple
from datetime import datetime
import requests



class Weather(BaseTool):
    name = "get_weather_info_api"
    is_remote = True
    description = "这是一个天气查询工具"

    def __call__(self,*agrs, **kwargs)->Tuple:
        """
        :param agrs:
        :param kwargs:
        :return:
        """
        self.default_city=[self._located_city]
        self.default_date=[self._set_date]

        city=kwargs.get("city",self.default_city)
        date=kwargs.get("date",self.default_date)

        weather_info,code=self._get_weather_info(city,date)
        return weather_info,code

    def _get_weather_info(self,city_lst:List, date_lst:List):
        """
        :param city_lst:
        :param date_lst:
        :return:
        """
        result,code = self._call_weather(city_lst, date_lst)
        return result,code

    @retry(max_retry=1,delay=0)
    def _call_weather(self,city_lst, date_lst):
        """
        :param city_lst:
        :param date_lst:
        :return:
        """
        post_url = "http://172.31.205.27:32157/online-agent-tool/open/agent/query/weather"
        response = requests.post(post_url, json={"city": city_lst, "date": date_lst})
        if response.status_code == 200:
            result = response.json()
            return result['data']
        else:
            return {"result": "非常抱歉，网络异常，天气暂时无法查询"}


    @property
    def _located_city(self)->str:
        """
        :return:
        """
        city = "北京"
        return city

    @property
    def _set_date(self)->str:
        """
        :return:
        """
        today = datetime.today()
        formatted_date = today.strftime('%Y-%m-%d')
        return formatted_date






