# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : data_utils.py
# Time       ：2024/5/18 10:18
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
import json
from .utils import return_code

def check_dict(dict_string):
    token=dict_string.split(":")[0]
    dict_string=dict_string.replace(token+":","").strip()
    try:
        try:
            eval(dict_string)
        except:
            json.loads(dict_string)
        return True
    except:
        return False



@return_code
def parse_tracjectory(text,is_replace=False):
    def get_content(line, token):
        content = ""
        if line.startswith(token):
            if is_replace:
                line = line.replace(token, "")
            content += line.strip()
        return content

    process_data_lst,thought_lst,action_lst,param_lst,obs_lst,finish=[],[],[],[],[],[]
    pipeline=[thought_lst,action_lst,param_lst,obs_lst,finish]

    line_lst= [line.strip() for line in text.strip().split("\n") if line.strip()]
    token_lst = "Thought Action Action_Parameter Observation Finish".split(" ")

    for line in line_lst:
        if len(line)==0:
            continue
        line=line.replace("：", ":")

        for token,lst in zip(token_lst,pipeline):
            token=token+":"
            res=get_content(line, token)
            if len(res)>0:
                lst.append(res)
            else:
                continue

    assert len(action_lst)==len(param_lst)==len(obs_lst) and len(thought_lst)==len(action_lst)+1 \
           and len(finish)==1,"data is not right."

    for data in zip(thought_lst[0:-1],action_lst,param_lst,obs_lst):
        Thought,Action,Action_Parameter,Observation=data
        process_data_lst.append([Thought,Action,Action_Parameter,Observation])

    process_data_lst.append([thought_lst[-1],finish[0]])

    return process_data_lst