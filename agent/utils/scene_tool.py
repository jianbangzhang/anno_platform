# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : scene_tool.py
# Time       ：2024/4/3 9:44
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""

def tool_choose(id_string):
    scene_tools_dict={
            "1": [
                "get_weather_info_api",
                "calendar_api",
                "calculator_api",
                "complex_visualization_api"
            ],
            "2": [
                "get_bill_cost_in_month_api",
                "get_fee_balance_api",
                "calculator_api",
                "calendar_api",
                "complex_visualization_api"
            ],
            "3": [
                "get_fee_balance_api",
                "get_bill_cost_in_month_api",
                "calculator_api",
                "calendar_api",
                "complex_visualization_api"
            ],
            "4": [
                "get_subscribe_service_api",
                "get_bill_cost_in_month_api",
                "calculator_api",
                "calendar_api",
                "complex_visualization_api"
            ],
            "5": [
                "get_pay_history_api",
                "get_fee_balance_api",
                "get_bill_cost_in_month_api",
                "calculator_api",
                "calendar_api",
                "complex_visualization_api"
            ],
            "6": [
                "get_flow_info_api",
                "calculator_api",
                "calendar_api",
                "complex_visualization_api"
            ],
            "7": [
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
            "8":[
                "knowledge_retrieval_api",
                "calendar_api",
                "calculator_api"
            ],
            "9":[
                "global_connection_traval_api",
                "global_connection_zone_api",
                "knowledge_retrieval_api"
            ],
            "10":[
                "pay_living_expenses_api",
                "get_living_balance_info_api",
                "open_living_expenses_info_api",
                "knowledge_retrieval_api",
                "calendar_api"
            ],
            "11":[
                "multimedia_content_search_api",
                "multimedia_rank_search_api",
                "movie_ticket_api",
                "cinema_find_api"
            ]
        }

    return scene_tools_dict.get(id_string, None)

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

def window():
    string="""可选择的场景集合：
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
    """
    return string




def tool_choose_for_server(scene:str):
    tool_list=scene_tools_dict[scene]
    return tool_list




def get_scene(id):
    tool_map={'1': '天气查询', '2': '账单查询', '3': '话费查询', '4': '已定业务查询', '5': '充值查询',
              '6': '流量查询', '7': '业务质疑', '8': '名词解释', '9': '全球通',"10":"生活缴费","11":"影音阅"}
    id=str(id)
    return tool_map[id]


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
        "complex_visualization_api"
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
        "calculator_api",
        "calendar_api",
        "complex_visualization_api"
    ],
    "业务质疑": [
        "get_bill_cost_in_month_api",
        "get_subscribe_service_api",
        "get_fee_balance_api",
        "get_pay_history_api",
        "get_flow_info_api",
        "points_info_api",
        "calculator_api",
        "calendar_api",
        "complex_visualization_api",
        "knowledge_retrieval_api"
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
    "积分查询":[
        "points_info_api",
        "knowledge_retrieval_api",
        "calculator_api"
    ]
}