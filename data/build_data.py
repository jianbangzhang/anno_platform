# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : build_data.py
# Time       ：2024/5/18 10:31
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from utils.prompt_utils import *
from typing import List,Dict
from dataclasses import dataclass


@dataclass
class Plan:
    thought:str
    api_name:str
    param:Dict
    def build(self):
        think_process=f"Thought: {self.thought}"+single_splitter+f"Action: {self.api_name}"+ \
                    single_splitter+f"Action_Parameter: {self.param}"+single_splitter+end_token
        return think_process


@dataclass
class Observations:
    exec_res:Dict
    def build(self):
        result=f"Observation:{self.exec_res}"+end_token
        return result


@dataclass
class Finish:
    thought: str
    final_result: str
    def build(self):
        final=f"Thought: {self.thought}"+single_splitter+f"Finish: {self.final_result}"
        if not self.final_result.strip().endswith("<end>"):
            final+=end_token
        return final


class DataStructure(object):
    def __init__(self,tool_list):
        self.tool_list=tool_list
        self.system=system_token+system
        self.available_tool_string=available_tool_string
        self.plan_requirements=plan_requirements


    def build_system(self,question):
        system_template=""
        system_template+=self.system+single_splitter
        system_template+=self.available_tool_string+single_splitter+"\n".join(self.tool_list)+single_splitter
        system_template+=self.plan_requirements+double_splitter
        system_template+=question
        system_template=system_template.replace("\n",splitter_token)
        return system_template


    def build_one_data_with_tool_call(self,question,process_lst: List[List]):
        plugin_content_list = []
        group_mask_flags = []
        plugin_content_list.append(question)
        group_mask_flags.append(1)

        for process in process_lst[0:-1]:
            thought, api_name, param, exec_res = process
            reason = Plan(thought, api_name, param)
            observations = Observations(exec_res)
            think_process = reason.build()
            think_process=think_process.replace("\n",splitter_token)
            plugin_content_list.append(think_process)
            group_mask_flags.append(0)
            subresult = observations.build()
            plugin_content_list.append(subresult)
            group_mask_flags.append(1)
        thought, final = process_lst[-1]
        finish = Finish(thought, final)
        final_res = finish.build()
        final_res = final_res.replace("\n", splitter_token)
        plugin_content_list.append(final_res)
        group_mask_flags.append(0)
        return plugin_content_list,group_mask_flags

    def build_one_data_without_tool_call(self, question,process_lst: List[List]):
        plugin_content_list = []
        group_mask_flags = []

        plugin_content_list.append(question)
        group_mask_flags.append(1)

        thought, final = process_lst[-1]
        finish = Finish(thought, final)
        final_res = finish.build()
        final_res = final_res.replace("\n", splitter_token)
        plugin_content_list.append(final_res)
        group_mask_flags.append(0)
        return plugin_content_list, group_mask_flags

    def build_multi_data(self,multi_turns_lst):
        """
        support multi-turn zero-call or multi-turn multi-call
        :param multi_turns_lst: [[question,[process_lst]],[question,[process_lst]],...]
        :return:
        """
        conversation_lst=[]
        flag_lst=[]
        for i,(question,data_lst) in enumerate(multi_turns_lst):
            question=question.replace("Question:","").replace("Question：","").strip()
            if i==0:
                question = question_format(question)
                question=self.build_system(question)
            else:
                question=f"""<User> {question}<end><Bot> """
            if len(data_lst)>1:
                plugin_content_list, group_mask_flags=self.build_one_data_with_tool_call(question,data_lst)
            else:
                plugin_content_list, group_mask_flags=self.build_one_data_without_tool_call(question,data_lst)

            conversation_lst += plugin_content_list
            flag_lst += group_mask_flags
        return conversation_lst,flag_lst

    def build_single_data(self,single_turns_lst):
        '''
        support single-turn multi-call or single-turn zero-call
        :param single_turns_lst: [[question,[process_lst]]]
        :return:
        '''
        conversation_lst = []
        flag_lst = []
        for i, (question, data_lst) in enumerate(single_turns_lst):
            question = question.replace("Question:", "").replace("Question：", "").strip()
            question = question_format(question)
            question = self.build_system(question)

            if len(data_lst) > 1:
                plugin_content_list, group_mask_flags = self.build_one_data_with_tool_call(question, data_lst)
            else:
                plugin_content_list, group_mask_flags = self.build_one_data_without_tool_call(question, data_lst)

            conversation_lst += plugin_content_list
            flag_lst += group_mask_flags
        return conversation_lst, flag_lst
