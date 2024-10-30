# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : __init__.py.py
# Time       ：2024/5/17 17:19
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
import json
from .parse_trajectory import parse_chat_text
from .build_data import DataStructure
from .process_data import transform_data,parse_save_data
from .check_data import check_agent_data,check_data_error,save_agent_data
from .send_data import transform_json_to_xlsx,perform_analysis,transform_data,parse_save_data,readJsonLines


def build_single_data(single_data_lst, tool_lst):
    """
    :param single_data_lst: [[question,[process_lst]]]
    :param tool_lst:
    :return:
    """
    one_data = {}
    ds = DataStructure(tool_lst)
    conversation_lst, flag_lst = ds.build_single_data(single_data_lst)

    one_data["plugin_content_list"] = conversation_lst
    one_data["group_mask_flags"] = flag_lst
    one_data["history"] = True
    one_data=json.dumps(one_data,ensure_ascii=False)
    return one_data



def build_multi_data(multi_data_lst, tool_lst):
    """
    :param multi_data_lst: [[question,[process_lst]],[question,[process_lst]],...]
    :param tool_lst:
    :return:
    """
    one_data = {}
    ds = DataStructure(tool_lst)
    conversation_lst, flag_lst = ds.build_multi_data(multi_data_lst)

    one_data["plugin_content_list"] = conversation_lst
    one_data["group_mask_flags"] = flag_lst
    one_data["history"] = True
    one_data=json.dumps(one_data,ensure_ascii=False)
    return one_data


def build_data(data_lst, tool_lst):
    """
    :param data_lst: [[question,[process_lst]],[question,[process_lst]],...]
    :param tool_lst:
    :return:
    """
    one_data = {}
    ds = DataStructure(tool_lst)
    conversation_lst, flag_lst = ds.build_multi_data(data_lst)

    one_data["plugin_content_list"] = conversation_lst
    one_data["group_mask_flags"] = flag_lst
    one_data["history"] = True
    one_data=json.dumps(one_data,ensure_ascii=False)
    return one_data
