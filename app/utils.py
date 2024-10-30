# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : utils.py.py
# Time       ：2024/5/30 17:31
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
import os
import json
import glob

user_json_file="datasets/user_info/usr.json"


def load_users():
    os.makedirs(os.path.dirname(user_json_file),exist_ok=True)
    if os.path.exists(user_json_file):
        with open(user_json_file, 'r',encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(user_json_file, 'w', encoding="utf-8") as f:
            json.dump({}, f)
        return {}


def save_users(users):
    exists_dict=load_users()
    if len(exists_dict)>0:
        exists_dict.update(users)
        with open(user_json_file, 'w',encoding="utf-8") as f:
            json.dump(exists_dict, f, ensure_ascii=False)
    else:
        with open(user_json_file, 'w',encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False)



def validate_username(username):
    return len(username) >= 3 and len(username) <= 20


def validate_password(password):
    return len(password) >= 8 and len(password) <= 20


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx'}


def conbine(lst1, lst2,result_lst):
    conbine_lst=[]
    result_list=[]
    for x, y,result in zip(lst1, lst2,result_lst):
        if isinstance(x, str) and isinstance(y, str):
            text=str(x).replace("<User>","").replace("<Bot>","").replace("<end>","").replace("：",":").strip()
            if not text.startswith("Question:"):
                text="Question:"+text
            text+="\n" + str(y).replace("<end>","").replace("：",":")
            conbine_lst.append(text)
            result_list.append(result)
        else:
            continue
    return conbine_lst,result_lst



def writeJsonl(data,jsonl_file):
    with open(jsonl_file, 'a', encoding='utf-8') as f:
        for entry in data:
            f.write(json.dumps(entry,ensure_ascii=False) + '\n')


def readJsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data


async def readJson(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

async def writeJson(data,jsonl_file):
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for entry in data:
            f.write(json.dumps(entry,ensure_ascii=False) + '\n')


def transform_data(data_string):
    data_string="\n".join([line.strip() for line in data_string.split("\n") if line.strip()])
    data_string=data_string.replace("Thought","\nThought").replace("Observation","\nObservation")
    return data_string

def save_excel_to_json(data_content,dataset_type,json_path):
    col_name_lst=data_content.columns.tolist()
    if "agent-split" in dataset_type:
        if not all([True if name in col_name_lst else False for name in ["query","trajectory"]]):
            code =-1
            return code
        query_lst=data_content["query"].to_list()
        traj_lst=data_content["trajectory"].to_list()
        if "result" in col_name_lst:
            result_lst=data_content["result"].to_list()
        else:
            result_lst=["" for _ in range(len(traj_lst))]

        if "error" in col_name_lst:
            error_lst = data_content["error"].to_list()
        else:
            error_lst = ["" for _ in range(len(traj_lst))]

        if "error_text" in col_name_lst:
            error_text_lst = data_content["error_text"].to_list()
        else:
            error_text_lst = ["" for _ in range(len(traj_lst))]

        data_lst,result_lst=conbine(query_lst,traj_lst,result_lst)
    else:
        if "data" not in col_name_lst:
            code=-2
            return code
        data_lst=data_content["data"].to_list()
        if "result" in col_name_lst:
            result_lst=data_content["result"].to_list()
        else:
            result_lst=["" for _ in range(len(data_lst))]

        if "error" in col_name_lst:
            error_lst = data_content["error"].to_list()
        else:
            error_lst = ["" for _ in range(len(data_lst))]

        if "error_text" in col_name_lst:
            error_text_lst = data_content["error_text"].to_list()
        else:
            error_text_lst = ["" for _ in range(len(data_lst))]


    for id,(data_string,result,error,error_text) in enumerate(zip(data_lst,result_lst,error_lst,error_text_lst)):
        one_data={}
        try:
            if not isinstance(data_string,str):
                continue
            if not isinstance(result,str):
                result=""
            if not isinstance(error,str):
                error=""
            if not isinstance(error_text,str):
                error_text=[]
            data_string=data_string.replace("<ret>","\n").replace("<end>","\n").strip()
            data_string=transform_data(data_string)
            one_data["id"]=id+1
            one_data["text"]=data_string
            one_data["result"]=result
            one_data["annotated"]=True if len(result)>0 else False
            one_data["is_delete"]=False
            one_data["error"]=error if len(error)>0 else ""
            one_data["error_text"]=[error_text] if len(error_text)>0 else []
            writeJsonl([one_data],json_path)
        except Exception as e:
            print(str(e))
            print("数据出错：",data_string)
            continue
    code=0
    return code


def get_user_file_path(username):
    user_folder=os.path.join('datasets', 'user_uploads', username)
    user_excel_dir=os.path.join(user_folder, "excel_files")
    user_json_dir = os.path.join(user_folder, "json_files")
    return user_excel_dir,user_json_dir




async def delete_remain_files(xlsx_file_dir,json_file_dir):
    xlsx_files = [os.path.basename(file) for file in glob.glob(os.path.join(xlsx_file_dir, '*.xlsx'))]
    json_files = [os.path.basename(file) for file in glob.glob(os.path.join(json_file_dir, '*.json'))]

    if len(xlsx_files)>len(json_files):
        to_delete = [file for file in xlsx_files if file not in json_files]

        for file in to_delete:
            file_path = os.path.join(xlsx_file_dir, file)
            os.remove(file_path)
            print(f"Deleted: {file_path}")
    elif len(xlsx_files) < len(json_files):
        to_delete = [file for file in json_files if file not in xlsx_files]
        for file in to_delete:
            file_path = os.path.join(json_file_dir, file)
            os.remove(file_path)
            print(f"Deleted: {file_path}")
    else:
        pass




