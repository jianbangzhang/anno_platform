# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : utils.py
# Time       ：2024/3/29 15:30
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
import json
import time
import pandas as pd
import os
import logging
import traceback
from datetime import datetime

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def retry(max_retry=3, delay=1):
    """
    :param max_retry:
    :param delay:
    :return:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry_count = 0
            result=""
            code=-1
            while retry_count < max_retry and code!=0:
                try:
                    result = func(*args, **kwargs)
                    code=0
                except Exception as e:
                    print(f"Exception occurred: {e}")
                    error = traceback.format_exc()
                    result={"error":str(error)}
                    code=-1
                    time.sleep(delay)
                retry_count+=1
            return result, code
        return wrapper
    return decorator


def getMsgFromText(text,token,filter_token):
    """
    :param text:
    :param token:
    :param filter_token:
    :return:
    """
    res=""
    text=text.replace("：",":").strip()
    if token in text:
        for line in text.split("\n"):
            line=line.strip()
            if line.startswith(token):
                res+=line
            else:
                continue

        if filter_token:
            res=res.replace(token,"").strip()
    else:
        res=text
    return res


def getFinishFromText(text,token="Finish",filter_token=True):
    """
    :param text:
    :param token:
    :param filter_token:
    :return:
    """
    res=""
    text=text.replace("：",":").strip()
    text_list=[t.strip() for t in text.split("\n") if t.strip()]
    if token in text:
        if token in text_list[-1]:
            for line in text_list:
                if line.startswith(token):
                    res+=line
                else:
                    continue
        else:
            for i in range(len(text_list)):
                line=text_list[i]
                if line.startswith(token):
                    res+="\n".join(text_list[i:])
                else:
                    continue

        if filter_token:
            res=res.replace(token,"").strip()
    else:
        res=text
    return res


def get_tool_prompts(tool_list,tool_dict):
    """
    :param tool_list:
    :param tool_dict:
    :return:
    """
    total_tools = []
    for tool in tool_list:
        api = tool_dict[tool]
        api_string = json.dumps(api, ensure_ascii=False)
        total_tools.append(api_string)
    return "\n".join(total_tools)

def checkOutput(string,TokenList)->bool:
    """
    :param string
    :param TokenList:
    :return:
    """
    signList=[]
    string=string.strip()
    for token in TokenList:
        if token in string:
            sign=True
        else:
            sign=False
        signList.append(sign)
    return all(signList)





def setLogWithTime():
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    project_directory = os.path.dirname(current_directory)

    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    os.makedirs(f"{project_directory}/logger",exist_ok=True)
    logging.basicConfig(
        filename=f'{project_directory}/logger/run.log',
        level=logging.INFO,
        format=log_format,
        datefmt=date_format
    )

def setLog(name=None):
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    project_directory = os.path.dirname(current_directory)

    log_format = '%(levelname)s - %(message)s'

    current_date = datetime.now().strftime('%Y-%m-%d')
    if name is None:
        log_filename = f'run_{current_date}.log'
    else:
        log_filename = f"{name}_{current_date}.log"


    os.makedirs(f"{project_directory}/logger", exist_ok=True)
    logging.basicConfig(
        filename=f'{project_directory}/logger/{log_filename}',
        level=logging.INFO,
        format=log_format
    )



def call_remote_agent(llm_input):
    """
    :param llm_input:
    :return:
    """
    from websockets.sync.client import connect
    import json

    # auth_url = "ws://172.29.100.69:9979/turing/v3/gpt"  # 华为
    auth_url="ws://36.138.59.240:9999/turing/v3/gpt" # a100

    prompt = {
        "header": {
            "traceId": "SPARK_DEMO"
        },
        "parameter": {
            "chat": {
                "temperature": 0,
                "max_tokens": 4096,
                "top_k": 1
            }
        },
        "payload": {
            "message": {
                "text": [
                    {"role": "user", "content": llm_input}
                ]
            }
        }
    }


    message = json.dumps(prompt, ensure_ascii=False)
    with connect(auth_url) as ws:
        response = ""
        ws.send(message)
        for res in ws:
            result = json.loads(res)
            try:
                response += result["payload"]["choices"]["text"][0]["content"]
                response=response.replace("<ret>","\n")
            except Exception as e:
                return e
    return response


def readJson(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def saveJson(path,data):
    with open(path, 'w',encoding='utf-8') as json_file:
        json.dump(data, json_file,ensure_ascii=False)
    print(f"数据已保存到 {path}")


def show_data_format(text,format="\t\t"):
    """
    :param text:
    :param format:
    :return:
    """
    text=str(text).replace("<ret>","\n")
    string=""
    for line in str(text).split("\n"):
        line=line.strip()
        if line:
            line=format+line
            string+=line+"\n"
        else:
            continue
    return string




def get_stream_result(stream_data_generator):
    """
    :param stream_data_generator:
    :return:
    """
    string=""
    try:
        data = next(stream_data_generator)
        string+=data+"\n"
        data=show_data_format(data)
        print(data)
    except StopIteration:
        print("Stream ended.")
    return string

def readJsonLines(path):
    """
    :param path:
    :return:
    """
    total_data=[]
    with open(path,"r",encoding="utf-8") as f:
        for line in f:
            data=json.loads(line)
            total_data.append(data)
    return total_data

def writeJsonLines(res_list,file_out_path):
    """
    :param res_list:
    :param file_out_path:
    :return:
    """
    with open(file_out_path, "a", encoding="utf-8") as f:
        for d in res_list:
            f.writelines(json.dumps(d,ensure_ascii=False)+"\n")
    print(f"saved to {os.path.abspath(file_out_path)}")


def transform(lst):
    total_data=[]
    for data in lst:
        data=data.strip()
        if data:
            if "\n" in data:
                lst=data.split("\n")
                lst=[e.strip() for e in lst if e.strip()]
                total_data+=lst
            else:
                total_data.append(data)
        else:
            continue
    total_data=[line+"\n"+"<end>" if line.startswith("Action_Parameter") else line for line in total_data]
    return total_data



def parse_llm_out(llm_out,one_dict):
    if all(True if token in llm_out else False for token in ["Thought", "Action", "Action_Parameter"]):
        thought = getMsgFromText(llm_out, "Thought:", filter_token=True)
        action = getMsgFromText(llm_out, "Action:", filter_token=True)
        action_parameter = getMsgFromText(llm_out, "Action_Parameter:", filter_token=True)
        one_dict["Thought"] =thought
        one_dict["Action"] =action
        one_dict["Action_Parameter"]= action_parameter

    if all(True if token in llm_out else False for token in ["Thought", "Finish"]):
        thought = getMsgFromText(llm_out, "Thought:", filter_token=True)
        finish = getMsgFromText(llm_out, "Finish:", filter_token=True)
        one_dict["Thought"]=thought
        one_dict["Finish"]= finish
    return one_dict


def categorized_xlsx(dir=r"D:\myproject\zhongyiAPP-Agent\agent_v2\data\final"):
    import os
    import pandas as pd
    from natsort import natsorted

    files = natsorted([f for f in os.listdir(dir) if f.endswith('.xlsx')])

    data_dict = {'充值查询': [], '话费查询': [], '已定业务查询': [],'账单查询':[],'综合业务质疑':[]}

    for file in files:
        file_path=os.path.join(dir,file)
        df = pd.read_excel(file_path)
        category = file.split("_")[0]
        data_dict[category].append(df)

    for category, data_list in data_dict.items():
        combined_df = pd.concat(data_list)
        combined_df.to_excel(fr"D:\myproject\zhongyiAPP-Agent\agent_v2\data\output\{category}_all.xlsx", index=False)


tool_dataset={
        "get_bill_cost_in_month_api":[],
        "get_subscribe_service_api":[],
        "get_flow_info_api":[],
        "points_info_api":[],
        "get_fee_balance_api":[],
        "get_pay_history_api":[],
    }


def get_api_and_obervation(trajectory,tool_dataset):
    """"
    :param trajectory:
    :param tool_dataset:
    :return:
    """

    trajectory=trajectory.replace("：",":")
    lst=[line.strip() for line in trajectory.split("Thought:") if line.strip()]

    for block in lst:
        block_lst=[line.strip() for line in block.split("\n") if line.strip()]
        block_lst=[line.replace("Action:","").replace("Observation:","").strip() for line in block_lst if line.startswith("Action:") or line.startswith("Observation:")]
        if len(block_lst)==2:
            try:
                tool,observation=block_lst
                if tool in tool_dataset:
                    observation_dict=eval(block_lst[-1])
                    if str(observation_dict) not in tool_dataset[tool]:
                        tool_dataset[tool].append(str(observation_dict))
            except:
                continue
        else:
            continue
    return tool_dataset




def transform_time(ans,api,time_param):
    import random
    from datetime import datetime,timedelta

    if api=="get_bill_cost_in_month_api":
        if len(time_param["year_month"])==1:
            year=time_param["year_month"][0]["year"] if len(time_param["year_month"][0]["year"])>0 else "2023"
            month=time_param["year_month"][0]["month"] if len(time_param["year_month"][0]["month"])>0 else "04"
            if len(month)==1: month="0"+month
            ans["result"][0]["month"]=year+"-"+month
        else:
            from copy import deepcopy
            if len(time_param["year_month"])>len(ans["result"]):
                diff=len(time_param["year_month"])-len(ans["result"])
                for _ in range(diff):
                    tmp=deepcopy(ans["result"][-1])
                    ans["result"].append(tmp)

            for i in range(len(time_param["year_month"])):
                year = time_param["year_month"][i]["year"] if len(time_param["year_month"][0]["year"]) > 0 else "2023"
                month = time_param["year_month"][i]["month"] if len(time_param["year_month"][0]["month"]) > 0 else "04"
                if len(month) == 1: month = "0" + month
                ans["result"][i]["month"] = year + "-" + month

    elif api=="get_pay_history_api":
        if len(time_param)==0:
            ans=ans
        else:
            try:
                date_string = time_param["result"]["date"]
                date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
                month=random.randint(1,6)
                months_ago = date_obj - timedelta(days=month * 30)
                ans["result"][0]["payDate"] = str(months_ago)
            except:
                ans=ans
    elif api=="get_subscribe_service_api":
        if len(time_param)==0:
            ans=ans
        else:
            try:
                date_string=time_param["result"]["date"]
                date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
                date_only = date_obj.date()
                month = random.randint(1, 6)
                three_months_ago = date_only - timedelta(days=month * 30)
                one_year_later = date_only + timedelta(days=365)
                ans["result"][0]["subscription_date"]=str(three_months_ago)
                ans["result"][0]["end_date"]=str(one_year_later)
            except:
                ans=ans
    else:
        raise NotImplementedError
    return ans


def get_time_from_llm_input(llm_input):
    llm_input=llm_input.replace("：",":")
    lst=reversed(llm_input.split("Thought:"))
    time_param={}
    for data in lst:
        if "Action:" in data and "Action_Parameter:" in data and "Observation:" in data and "calendar_api" in data:
            data_lst=[line.strip() for line in data.split("<ret>") if line.strip()]
            calendar_lst=[line.replace("Observation:","").strip() for line in data_lst if line.startswith("Observation:")]
            if calendar_lst:
                calendar_result=calendar_lst[-1]
                time_param=eval(calendar_result)
            else:
                continue
        else:
            continue
    return time_param


def get_history_text(record_list):
    data_lst=record_list[-1]
    last_rounds = list(data_lst.keys())[-1]
    llm_input = data_lst[last_rounds]["LLM_INPUT"]
    llm_input=llm_input.replace("<end><Bot>","<end><Bot>\n").replace("\n<end>","\n<end>\n").replace("<end>Observation","<end>\nObservation")
    llm_output = data_lst[last_rounds]["LLM_OUTPUT"]

    history = llm_input.split("接下来开始对话：")[-1].strip().replace("<ret>", "\n").replace("\n\n","") + llm_output
    return history



def get_scene_from_xlsx_name(file_name):
    scene_list = ['天气查询', '账单查询',  '话费查询', '已订业务查询','充值查询',
                '流量查询','业务质疑', '名词解释', '全球通', "生活缴费", "影音阅"]
    for s in scene_list:
        if s in file_name:
            return s
        else:
            continue










def transform2excel(input_folder,output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    all_data = pd.DataFrame()

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename.replace('.json', '.xlsx'))
            data = readJsonLines(input_file_path)

            df = pd.DataFrame(data)

            df.to_excel(output_file_path, index=False)

            all_data = pd.concat([all_data, df], ignore_index=True)

    all_data_file_path = os.path.join(output_folder, 'total_data.xlsx')
    all_data.to_excel(all_data_file_path, index=False)

    print("所有JSON文件已转换为Excel文件，并且已保存到一个总的Excel文件中。")


def save_into_groups(input_folder,output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    category_data = {}

    for filename in os.listdir(input_folder):
        if filename.endswith('.xlsx'):
            input_file_path = os.path.join(input_folder, filename)
            category = filename.split('_')[1]

            df = pd.read_excel(input_file_path)

            if category in category_data:
                category_data[category] = pd.concat([category_data[category], df], ignore_index=True)
            else:
                category_data[category] = df

    for category, df in category_data.items():
        if category.endswith("xlsx"):
            category=category.split(".")[0]
        output_file_path = os.path.join(output_folder, f'merged_{category}.xlsx')
        df.to_excel(output_file_path, index=False)

    print("所有文件已按类别合并并保存到相应的Excel文件中。")






