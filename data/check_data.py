# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : check_data.py
# Time       ：2024/7/2 10:53
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""

import json
from agent.utils import new_api_map,readJsonLines
from data.parse_trajectory import parse_chat_text



def extract_keys(d, keys_list=None):
    if keys_list is None:
        keys_list = []
    for key, value in d.items():
        keys_list.append(key)
        if isinstance(value, dict):
            extract_keys(value, keys_list)
    return keys_list


def get_param(new_dict):
    tool_param = {}
    for tool in new_dict:
        params_tool = {"action": [], "observation": []}
        params = new_dict[tool]
        action_param = params["parameters"]
        observation_param = params["return_description"]["result"]
        if len(action_param) == 0:
            params_tool["action"].append("none")
        else:
            for d in action_param:
                action_p = d["name"]
                params_tool["action"].append(action_p)

        if isinstance(observation_param, list):
            for d in observation_param:
                params_tool["observation"].extend(list(d.keys()))
        elif isinstance(observation_param, dict):
            params_tool["observation"].extend(list(observation_param.keys()))
        elif isinstance(observation_param, str):
            params_tool["observation"].append("str")
        else:
            print("解析工具的出参和入参出错", observation_param)
        tool_param[tool] = params_tool
    return tool_param






def check_trajectory(data,tool_name_lst,tool_param,error_text):
    message=""
    for call, e_lst in enumerate(data):
        if len(e_lst) == 4:
            if e_lst[0].startswith("Thought") and e_lst[1].startswith("Action:") and e_lst[2].startswith("Action_Parameter") and e_lst[3].startswith("Observation"):
                tool_name = e_lst[1].replace("Action:", "").strip()
                param_dict = e_lst[2].replace("Action_Parameter:", "").strip()
                observation_dict = e_lst[3].replace("Observation:", "").strip()

                if tool_name not in tool_name_lst:
                    error_text.append(tool_name)
                    message +="\n"+f"工具选择错误：\n工具->{tool_name}不在工具集->{'、'.join(tool_name_lst)}"
                    print(f"工具选择错误：\n工具->{tool_name}不在工具集->{'、'.join(tool_name_lst)}")
                    continue

                normal_action_param = tool_param[tool_name]["action"]
                normal_observation_param = tool_param[tool_name]["observation"]
                normal_observation_param.append("result")
                normal_observation_param.append("回复话术")
                normal_observation_param.append("提醒")
                normal_observation_param.append("提醒事项")

                try:
                    try:
                        param_dict=json.loads(param_dict)
                    except:
                        param_dict=eval(param_dict)
                except:
                    error_text.append(str(param_dict))
                    print(f"json格式出错：Action_Parameter->{param_dict}不是合法的JSON格式")
                    message += "\n" +f"json格式出错：\nAction_Parameter->{param_dict}不是合法的JSON格式"


                try:
                    try:
                        observation_dict=json.loads(observation_dict)
                    except:
                        observation_dict=eval(observation_dict)
                except:
                    print(f"json格式出错：Observation->{observation_dict}不是合法的JSON格式")
                    message+="\n"+f"json格式出错：\nObservation->{observation_dict}不是合法的JSON格式"
                    error_text.append(str(observation_dict))

                if 'none' in normal_action_param:
                    if len(param_dict)>0:
                        message+="\n"+f"工具->{tool_name}无入参"
                        error_text.append(str(param_dict))
                        print(f"工具{tool_name}无入参")
                else:
                    if not all([True if t in str(param_dict) else False for t in normal_action_param]):
                        print(f"工具->{tool_name}入参缺失：其正确参数有：{'、'.join(normal_action_param)}，")
                        not_in_param = [t for t in normal_action_param if t not in str(param_dict)]
                        print(f"现在入参->{param_dict}缺少参数：{'、'.join(not_in_param)}")
                        message+="\n"+f"工具->{tool_name}入参缺失：其正确参数有：{'、'.join(normal_action_param)},\n"+f"现在入参->{str(param_dict)}缺少参数：{'、'.join(not_in_param)}"
                        error_text.append(str(param_dict))

                if "str" not in normal_observation_param:
                    observation_lst=extract_keys(observation_dict)
                    if not all([True if t in normal_observation_param else False for t in observation_lst]):
                        print(f"工具{tool_name}出参错误：其正确参数有：{'、'.join(normal_observation_param)}，")
                        error_param = [t for t in observation_lst if t not in normal_observation_param]
                        print(f"现在出参{observation_dict}错误：{'、'.join(error_param)}")
                        error_text.append(str(observation_dict))
                        message += "\n"+f"工具->{tool_name}出参错误：其正确参数有：{'、'.join(normal_observation_param)}，\n"+f"现在出参->{observation_dict}错误：{'、'.join(error_param)}"
                else:
                    pass
            else:
                plan='\n'.join(e_lst)
                print(f"智能体规划出错：\n{plan}")
                message+="\n"+f"智能体规划出错：\n{plan}"
                error_text.append(str(plan))

        elif len(e_lst) == 2:
            if e_lst[0].startswith("Thought") and e_lst[1].startswith("Finish"):
                pass
            else:
                ans = '\n'.join(e_lst)
                print(f"智能体回复出错：\n{ans}")
                message += "\n" + f"智能体回复出错：\n{ans}"
                error_text.append(str(ans))
        else:
            content='\n'.join(e_lst)
            print(f"内容出错：{content}\t不是智能体规划，也不是智能体回复！")
            message+="\n"+f"内容出错：{content}\t不是智能体规划，也不是智能体回复！"
            error_text.append(content)
    error_text=list(set(error_text))
    return message,error_text


async def writeJsonLines(res_list,file_out_path):
    """
    :param res_list:
    :param file_out_path:
    :return:
    """
    with open(file_out_path, "w", encoding="utf-8") as f:
        for d in res_list:
            f.writelines(json.dumps(d,ensure_ascii=False)+"\n")



async def check_agent_data(json_file):
    total_data=readJsonLines(json_file)
    tool_param=get_param(new_api_map)

    tool_name_lst=list(new_api_map.keys())
    for i,data in enumerate(total_data):
        text=data["text"]

        blocklst,code=parse_chat_text(text)
        data_msg = ""
        error_text=[]
        if code!=0:
            print("交互过程出错")
            data_msg="\n"+"交互过程出错"

        for round in range(len(blocklst)):
            round_data=blocklst[round]
            for data in round_data:
                if isinstance(data,str):
                   pass
                elif isinstance(data,list):
                    msg,error_text=check_trajectory(data,tool_name_lst,tool_param,error_text)
                    data_msg+=f"第{round+1}轮对话出现问题->"+msg if len(msg)>0 else ""
                else:
                    pass
        if len(total_data[i]["error"])==0:
            total_data[i]["error"]=data_msg
        else:
            if data_msg!=total_data[i]["error"]:
                total_data[i]["error"]+=data_msg
            else:
                total_data[i]["error"]=data_msg

        if len(total_data[i]["error_text"])==0:
            total_data[i]["error_text"]=error_text
        else:
            if total_data[i]["error_text"] not in error_text:
                error_text.append(total_data[i]["error_text"])
                total_data[i]["error_text"]=error_text
            else:
                total_data[i]["error_text"] = error_text
    await writeJsonLines(total_data,json_file)



async def check_data_error(json_file,id,text):
    total_data = readJsonLines(json_file)
    tool_param = get_param(new_api_map)

    tool_name_lst = list(new_api_map.keys())
    blocklst, code = parse_chat_text(text)
    data_msg = ""
    error_text = []
    if code != 0:
        print("交互过程出错")
        data_msg = "\n" + "交互过程出错"
        error_text.append("交互过程出错")

    for round in range(len(blocklst)):
        round_data = blocklst[round]
        for data in round_data:
            if isinstance(data, str):
                pass
            elif isinstance(data, list):
                msg, error_text = check_trajectory(data, tool_name_lst, tool_param, error_text)
                data_msg += f"第{round + 1}轮对话出现问题->" + msg if len(msg) > 0 else ""
            else:
                pass
    total_data[id]["error"] = data_msg
    total_data[id]["error_text"] = error_text
    await writeJsonLines(total_data, json_file)
    if len(data_msg)>0 and len(error_text)>0:
        error_info="\n".join([str(i+1)+"."+str(data) for i,data in enumerate(error_text)])
        msg=f"出错：\n{error_info}\n\n错误原因：\n{data_msg}"
    else:
        msg="未发现数据错误"
    return msg



async def save_agent_data(json_file,data_id, text):
    id=int(data_id)-1
    total_data = readJsonLines(json_file)
    total_data[id]["result"] = text
    total_data[id]['annotated']=True
    msg=await check_data_error(json_file,id,text)
    if msg=="未发现数据错误":
        total_data[id]["error"] = ""
    await writeJsonLines(total_data,json_file)



