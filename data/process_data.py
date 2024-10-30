# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : process_data.py
# Time       ：2024/5/29 09:54
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""


def transform_data(text_lst):
    result=[]
    for rounds in text_lst:
        conversations=[]
        question=rounds[0]
        if question.startswith("Question"):
            question=question.replace("Question:","").strip()
        conversations.append({
            "type": "question",
            "content": [
                {"type": "input", "value": question, "prefix": "Question: "}
            ]
        })
        for lst in rounds[-1]:
            size=len(lst)
            if size==2:
                thought=lst[0].replace("Thought:","").strip()
                finish=lst[-1].replace("Finish:","").strip()
                conversations.append({
                    "type": "thoughtFinish",
                    "content": [
                        {"type": "input", "value": thought, "prefix": "Thought: "},
                        {"type": "input", "value": finish, "prefix": "Finish: "}
                    ]
                })
            elif size==4:
                thought = lst[0].replace("Thought:", "").strip()
                action=lst[1].replace("Action:", "").strip()
                param=lst[2].replace("Action_Parameter:", "").strip()
                observation=lst[3].replace("Observation:", "").strip()
                conversations.append(
                    {
                        "type": "thoughtAction",
                        "content": [
                            {"type": "input", "value": thought, "prefix": "Thought: "},
                            {"type": "input", "value": action},
                            {"type": "input", "value": str(param), "prefix": ""},
                            {"type": "textarea", "value": observation}
                        ]
                    }
                )
            else:
                raise ValueError

        result.append(conversations)
    return result


def add_token(text,token):
    text=text.replace("：",":").strip()
    token=token+":"
    if not text.startswith(token):
        text=token+text
    else:
        text=text
    return text.strip()


def check_data(data):
    total_code=[]
    for round_lst in data:
        code_lst=[]
        if round_lst:
            for i,data_dict in enumerate(round_lst):
                classify = data_dict["type"]
                if i==0:
                    if classify=="question":
                        code=0
                    else:
                        code=-2
                    code_lst.append(code)

                if i==len(round_lst)-1:
                    if classify=="thoughtFinish":
                        code=0
                    else:
                        code=-3
                    code_lst.append(code)

                if len(round_lst)>2 and i>0 and i<len(round_lst)-1:
                    if classify=="thoughtAction":
                        code=0
                    else:
                        code=-4
                    code_lst.append(code)
            total_code.append(code_lst)
        else:
            continue

    for i,code_lst in enumerate(total_code):
        if len(code_lst)==0:
            msg="请勿保存空对话！"
            code=-5
            return msg,code
        if len(code_lst)==1:
            msg="对话过程不完整！"
            code=-6
            return msg,code
        if -2 in code_lst:
            msg=f"第{i+1}轮对话的不是以question开头！"
            code=-2
            return msg,code
        if -3 in code_lst:
            msg = f"第{i + 1}轮对话的不是以Thought/Finish结束！"
            code = -3
            return msg, code
        if -4 in code_lst:
            msg = f"第{i + 1}轮对话的中间过程不是Thought/Action/Action_Parameter/Observation !"
            code = -4
            return msg, code
    code=0
    msg="数据完整，顺序正确"
    return msg,code


def parse_save_data(data):
    total_data=[]
    msg,code=check_data(data)
    if code!=0:
        return msg,code
    try:
        for round_lst in data:
            if round_lst:
                for data_dict in round_lst:
                    classify=data_dict["type"]
                    if classify=="question":
                        question=data_dict["content"][0]['value']
                        question=add_token(question,"Question")
                        total_data.append(question)
                    elif classify=="thoughtAction":
                        thought=data_dict["content"][0]['value']
                        thought=add_token(thought,"Thought")
                        action=data_dict["content"][1]['value']
                        action=add_token(action,"Action")
                        param=data_dict["content"][2]['value']
                        param=add_token(param,"Action_Parameter")
                        observation=data_dict["content"][3]['value']
                        observation=add_token(observation,"Observation")
                        total_data.append(thought)
                        total_data.append(action)
                        total_data.append(param)
                        total_data.append(observation)
                    elif classify=="thoughtFinish":
                        thought = data_dict["content"][0]['value']
                        thought = add_token(thought, "Thought")
                        finish = data_dict["content"][1]['value']
                        finish =add_token(finish,"Finish")
                        total_data.append(thought)
                        total_data.append(finish)
                    else:
                        continue
            else:
                continue
        code=0
        return "\n".join(total_data), code
    except:
        code=-1
        msg="数据处理失败"
        return msg,code


