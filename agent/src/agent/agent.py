# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : agent.py
# Time       ：2024/3/29 21:18
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from agent.message import ObservationMessage
from .base import BaseAgent
import logging
from agent.utils import setLog,show_data_format,get_stream_result,getFinishFromText,question_format
from agent.utils import parse_llm_out
import time

setLog()


class AppAgent(BaseAgent):
    def __init__(self,config,tool,llm,action,prompt_generator,**kwargs):
        """
        :param config:
        :param tool:
        :param llm:
        :param action:
        :param prompt_generator:
        :param kwargs:
        """
        super().__init__(config,tool,llm,action,prompt_generator,**kwargs)
        self.tool_config = config
        self.tool = tool
        self.action = action
        self.prompt_generator = prompt_generator
        self.kwargs = kwargs
        self.llm = llm

    def _init(self,question:str,tool_list=None):
        """
        :param question；
        :param tool_list
        """

        print("*"*120)
        init_prompt=self.prompt_generator.init_prompt(tool_list,question)
        return init_prompt


    def singleChatRun(self, query, is_stream_chat=True,*args,**kwargs):
        """
        :param query:
        :param is_stream_chat:
        :param args:
        :param kwargs:
        :return:
        """
        history_lst=[]
        tool_dict=kwargs.get("tool_dict",{})
        tool_list,llm_input=self._init(query,**tool_dict)
        final_answer=""
        is_final=False
        time_lst=[]
        record_lst=[]

        round=1
        while not is_final:
            record_dict={}
            one_dict={}
            print("ROUND:",round)
            print("*" * 120)
            print("\tLLM_INPUT:")
            if len(history_lst)>0:
                llm_input = self.prompt_generator.build_prompt(tool_list, query, history_lst)
            print(show_data_format(llm_input))
            one_dict["LLM_INPUT"]=llm_input
            logging.info(f"ROUND:{round}\n"+"*" * 120 + "\n" + "\tLLM_INPUT:\n"+show_data_format(llm_input))

            print()
            print("\tLLM_OUTPUT:")
            logging.info("\tLLM_OUTPUT:")

            start=time.time()
            if is_stream_chat:
                llm_out = self.llm.stream_chat(llm_input,is_remote=True)
                llm_out=get_stream_result(llm_out)
            else:
                llm_out = self.llm.chat(llm_input, is_remote=True)
                print(show_data_format(llm_out))
                logging.info(show_data_format(llm_out))

            time_diff = time.time() - start
            time_lst.append(time_diff)
            one_dict["LLM_OUTPUT"]=llm_out
            is_llm_output_valid,is_stop=self.llm.checkLLMOut(llm_out)
            history_lst.append(llm_out)

            print()
            one_dict=parse_llm_out(llm_out,one_dict)
            api, param_dict= self.action.get_api_param(llm_out)
            print("\tACTION:", api)
            print("\tACTION_PARAMETER:", param_dict)
            logging.info(f"\tACTION:{api}\n" + f"\tACTION_PARAMETER:{param_dict}")

            if (api is None and param_dict is None) or (is_stop and is_llm_output_valid):
                is_final=True
            else:
                is_final=False
                is_action_valid = self.action.check(self.tool)
                logging.info("\tCheck API and Params:"+f"{api}-{param_dict} is Vaild" if is_action_valid else f"{api}-{param_dict} is Not Vaild\n")

            if is_final:
                print()
                print("\tFINAL:")
                final_answer += getFinishFromText(llm_out,"Finish:",filter_token=True)
                print(show_data_format(llm_out))
                logging.info("\tFINAL:\n"+show_data_format(llm_out))
                print()
                if llm_out not in history_lst:
                    history_lst.append(llm_out)
            else:
                print()
                print("\tOBSERVATION:")
                start = time.time()
                if 'keywords' in param_dict:
                    param_dict['keyword'] = param_dict.pop('keywords')

                tool_result,code=self.tool.execute(api,**param_dict)
                tool_time=time.time()-start
                print(show_data_format(tool_result))
                logging.info("\tOBSERVATION:\n" + show_data_format(tool_result))
                print()
                if code==0:
                    observation=ObservationMessage.wrapper(tool_result)
                else:
                    print(f"工具调用失败,具体详情：api->{api},param->{param_dict}")
                    break
                history_lst.append(observation)
                one_dict["Observation"]=str(tool_result)
                one_dict["tool_time"] = tool_time
                logging.info("*" * 120 + "\n" + "observation:\n" + str(observation))
            print("*" * 120)
            one_dict["llm_time"]=time_diff
            record_dict[f"ROUND {round}"] = one_dict
            record_lst.append(record_dict)
            round+=1
            if round>=10:
                break
        return final_answer,history_lst,record_lst,time_lst





    def multiChatRun(self,query,history_lst,is_stream_chat=True,*args,**kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        tool_dict=kwargs.get("tool_dict",{})
        if len(tool_dict)==0:
            tool_list=[tool_dict["api"] for tool_dict in self.tool_config.tool_list if tool_dict["is_available"]]
        else:
            tool_list=tool_dict["tool_list"]

        current_chat_lst = []
        if len(history_lst)==0:
            llm_input=self._init(query,**tool_dict)
        else:
            llm_input = self.prompt_generator.build_multi_prompt(tool_list, query, history_lst,current_chat_lst)

        final_answer=""
        is_final=False
        current_chat_lst.append(question_format(query))
        round=1

        while not is_final:
            print("ROUND:",round)
            print("*" * 120)
            print("\tLLM_INPUT:")


            if len(current_chat_lst)>1 and len(history_lst)==0:
                llm_input = self.prompt_generator.build_prompt(tool_list, query, current_chat_lst)

            if len(current_chat_lst)>1 and len(history_lst)>0:
                llm_input = self.prompt_generator.build_multi_prompt_next_call(tool_list,history_lst,current_chat_lst)

            print(show_data_format(llm_input))
            logging.info(f"ROUND:{round}\n"+"*" * 120 + "\n" + "\tLLM_INPUT:\n"+show_data_format(llm_input))

            print()
            print("\tLLM_OUTPUT:")
            logging.info("\tLLM_OUTPUT:")

            if is_stream_chat:
                llm_out = self.llm.stream_chat(llm_input,is_remote=True)
                llm_out=get_stream_result(llm_out)
            else:
                llm_out = self.llm.chat(llm_input, is_remote=True)
                print(show_data_format(llm_out))
                logging.info(show_data_format(llm_out))

            is_llm_output_valid,is_stop=self.llm.checkLLMOut(llm_out)
            current_chat_lst.append(llm_out)

            print()
            api, param_dict= self.action.get_api_param(llm_out)
            print("\tACTION:", api)
            print("\tACTION_PARAMETER:", param_dict)
            logging.info(f"\tACTION:{api}\n" + f"\tACTION_PARAMETER:{param_dict}")

            if (api is None and param_dict is None) or (is_stop and is_llm_output_valid):
                is_final=True
            else:
                is_final=False
                is_action_valid = self.action.check(self.tool)
                logging.info("\tCheck API and Params:"+f"{api}-{param_dict} is Vaild" if is_action_valid else f"{api}-{param_dict} is Not Vaild\n")

            if is_final:
                print()
                print("\tFINAL:")
                final_answer += getFinishFromText(llm_out,"Finish:",filter_token=True)
                print(show_data_format(llm_out))
                logging.info("\tFINAL:\n"+show_data_format(llm_out))
                print()
                if llm_out not in current_chat_lst:
                    current_chat_lst.append(llm_out)
            else:
                print()
                print("\tOBSERVATION:")
                if 'keywords' in param_dict:
                    param_dict['keyword'] = param_dict.pop('keywords')

                tool_result,code=self.tool.execute(api,**param_dict)
                print(show_data_format(tool_result))
                logging.info("\tOBSERVATION:\n" + show_data_format(tool_result))
                print()
                if code==0:
                    observation=ObservationMessage.wrapper(tool_result)
                else:
                    print(f"工具调用失败,具体详情：api->{api},param->{param_dict}")
                    break
                current_chat_lst.append(observation)

                logging.info("*" * 120 + "\n" + "observation:\n" + str(observation))
            print("*" * 120)
            round+=1
            if round>=10:
                break

        history_lst.append(current_chat_lst)
        return final_answer,history_lst
        

