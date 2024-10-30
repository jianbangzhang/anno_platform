# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : utils.py
# Time       ：2024/5/18 10:21
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
import traceback
import json

def return_code(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            code=0
        except Exception as e:
            result=None
            code=-1
            print(f"Exception occurred: {e}")
            traceback.print_exc()
        return result, code

    return wrapper


def optional_scene():
    options = [
        "天气查询",
        "账单查询",
        "话费查询",
        "已订业务查询",
        "充值查询",
        "流量查询",
        "业务质疑",
        "名词解释",
        "全球通",
        "生活缴费",
        "影音阅"
    ]
    return options


scene_tools_dict={
    "天气查询": [
        "get_weather_info_api",
        "calendar_api",
        "calculator_api",
        "complex_visualization_api"
    ],
    "账单查询": [
        "get_bill_cost_in_month_api",
        "get_fee_balance_api",
        "calculator_api",
        "calendar_api",
        "visualization_api"
    ],
    "话费查询": [
        "get_fee_balance_api",
        "get_bill_cost_in_month_api",
        "calculator_api",
        "calendar_api"
    ],
    "已订业务查询": [
        "get_subscribe_service_api",
        "get_bill_cost_in_month_api",
        "calculator_api",
        "calendar_api"
    ],
    "充值查询": [
        "get_pay_history_api",
        "get_fee_balance_api",
        "get_bill_cost_in_month_api",
        "calculator_api",
        "calendar_api",
        "complex_visualization_api"
    ],
    "流量查询": [
        "get_flow_info_api",
        "get_bill_cost_in_month_api",
        "get_subscribe_service_api",
        "get_pay_history_api",
        "get_flow_info_api",
        "get_fee_balance_api",
        "calculator_api",
        "calendar_api",
        "complex_visualization_api"
    ],
    "业务质疑": [
        "get_bill_cost_in_month_api",
        "get_subscribe_service_api",
        "get_pay_history_api",
        "get_flow_info_api",
        "get_fee_balance_api",
        "points_info_api",
        "calculator_api",
        "calendar_api",
        "complex_visualization_api"
    ],
    "名词解释":[
        "knowledge_retrieval_api",
        "calendar_api",
        "calculator_api"
    ],
    "全球通":[
        "global_connection_traval_api",
        "global_connection_zone_api",
        "knowledge_retrieval_api"
    ],
    "生活缴费":[
        "pay_living_expenses_api",
        "get_living_balance_info_api",
        "open_living_expenses_info_api",
        "knowledge_retrieval_api",
    ],
    "影音阅":[
        "multimedia_content_search_api",
        "multimedia_rank_search_api",
        "movie_ticket_api",
        "cinema_find_api"
    ],
    "积分查询":["points_info_api",
            "knowledge_retrieval_api"
    ]
}


def pretty_window():
    string="""  
        可选择场景
_____________________________
        1.天气查询       
        2.账单查询       
        3.话费查询       
        4.已定业务查询    
        5.充值查询       
        6.流量查询       
        7.业务质疑       
        8.名词解释       
        9.全球通         
        10.生活缴费      
        11.影音阅        
_____________________________
    """
    return string



def transform_data(text_lst):
    import json
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
                conversations.append({
                    "type": "thoughtFinish",
                    "content": [
                        {"type": "input", "value": lst[0], "prefix": "Thought: "},
                        {"type": "input", "value": lst[-1], "prefix": "Finish: "}
                    ]
                })
            elif size==4:
                conversations.append(
                    {
                        "type": "thoughtAction",
                        "content": [
                            {"type": "input", "value": lst[0], "prefix": "Thought: "},
                            {"type": "input", "value": lst[1]},
                            {"type": "input", "value": json.dumps(lst[2],ensure_ascii=False), "prefix": ""},
                            {"type": "textarea", "value": lst[3]}
                        ]
                    }
                )
            else:
                raise ValueError

        result.append(conversations)
    return result



