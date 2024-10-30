# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : tools.py
# Time       ：2024/3/28 15:04
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""


new_api_map = {
    # 中移
    "get_bill_cost_in_month_api":
    {
        "tool": "账单查询工具",
        "api_name": "get_bill_cost_in_month_api",
        "api_description": "查询用户某个或多个月份的消费账单，返回内容包括当月的总消费金额，扣费项目和每项的扣费金额数据。",
        "parameters": [
            {
                "name": "year_month",
                "description": "用户需要查询的所有年月，每项必须是一个字典，其中month必填表示查询的月份，year选填表示查询的年份（默认值为""表示当前年份），month和year都必须是阿拉伯数字字符串，例如 [{'year':'2024','month':'4'}]",
                "type": "List[Dict]",
                "required": True
            }
        ],
        "return_description": {
            "result": [
                {
                    "month": "表示本项查询结果所属的年份和月份",
                    "total_bill": "本月总消费金额",
                    "actual_pay": "实际应付金额（指本月总消费金额剔除他人代付、活动返还、优惠金额后的实际支付费用）",
                    "save_bill": "本期账单的总优惠金额（包括减免金额，活动范费抵扣金额）",
                    "business_bill": "套餐及固定费用（指基础套餐、语音包、流量包、宽带、来电显示等固定费用）",
                    "outplan_bill": "套餐外消费（包括套餐外语音费、套餐外上网费、套餐外短/彩信费）",
                    "added_bill": "增值业务费（包括互联网电视、彩铃、视频彩铃、咪咕会员等）"
                }
            ],
            "提醒事项": "回答用户时，需要提醒用户的注意事项，例如是否产生超套消费等。"
        }
    },

    "get_subscribe_service_api":
    {
        "tool": "已订业务查询工具",
        "api_name": "get_subscribe_service_api",
        "api_description": "用于查询获取用户套餐中包含的已订购业务的详细信息",
        "parameters": [],
        "return_description": {
            "result": [
                {
                    "service_name": "订购的业务名称",
                    "subscription_date": "业务订购日期",
                    "end_date": "业务结束时间"
                }
            ]
        }
    },


    "get_fee_balance_api":
    {
        "tool": "话费查询工具",
        "api_name": "get_fee_balance_api",
        "api_description": "查询账户内当前可用余额与本月已消费金额。",
        "parameters": [],
        "return_description": {
            "result": {
                    "left_money": "账户可用余额",
                    "used_money": "本月已消费金额",
                },
            "提醒事项": "回答用户时，需要提醒用户的注意事项，例如是否话费不足等。"
        }
    },

    "get_pay_history_api":
    {
        "tool": "充值记录查询工具",
        "api_name": "get_pay_history_api",
        "api_description": "查询获取用户历史充值记录信息。",
        "parameters": [],
        "return_description": {
            "result": [
                {
                    "amount": "充值金额",
                    "payType": "充值方式",
                    "payDate": "充值时间"
                }
            ]
        }
    },

    "get_flow_info_api":
    {
        "tool": "流量查询工具",
        "api_name": "get_flow_info_api",
        "api_description": "查询用户本月流量使用情况，返回内容包含本月不同类型的流量总数、已使用量、剩余量。",
        "parameters": [],
        "return_description": {
            "result": [
                {
                    "resource_unit": "资源单位",
                    "remaining_amount": "流量剩余",
                    "total_amount": "流量总量",
                    "used_amount": "流量已使用量",
                    "flow_category": "流量类型"
                }
            ],
            "提醒事项": "回答用户时，需要提醒用户的注意事项，例如是否流量不足等。"
        }
    },

    "points_info_api":
    {
        "tool": "积分查询工具",
        "api_name": "points_info_api",
        "api_description": "查询用户账户内当前可用积分总量。",
        "parameters": [],
        "return_description": {
            "result": {"totalPoint": "账户内积分总量"}
        }
    },

    "visualization_api":
    {
        "tool": "绘图工具",
        "api_name": "visualization_api",
        "api_description": "根据输入的横纵坐标和数值，绘制一张二维图表",
        "parameters": [
            {
                "name": "x",
                "description": "横轴数据，例如 ['一月', '二月', '三月']",
                "type": "List[str]",
                "required": True
            },
            {
                "name": "y",
                "description": "纵轴数据，例如 ['100', '150', '93']",
                "type": "List[str]",
                "required": True
            },
            {
                "name": "labels",
                "description": "横轴和纵轴的图例，例如 {'x':'月份', 'y':'消费金额（元）'}",
                "type": "dict",
                "required": True
            }
        ],
        "return_description": {
            "result": "是否绘图成功的信号"
        }
    },

    "calendar_api":
    {
        "tool": "日期查询工具",
        "api_name": "calendar_api",
        "api_description": "将口语表达的时间转换为标准格式的日期。",
        "parameters": [
            {
                "name": "date",
                "description": "日期或时间的模糊口语表达",
                "type": "str",
                "required": True
            }
        ],
        "return_description": {
            "result": {
                "date": "转换后的日期，为'yyyy-mm-dd'的格式",
                "星期": "这天是星期几"
            }
        }
    },

    "calculator_api":
    {
        "tool": "计算器工具",
        "api_name": "calculator_api",
        "api_description": "根据提供的数学表达式计算出正确的数值结果，适用于需要计算差值、总量、均值等等场景",
        "parameters": [
            {
                "name": "expression",
                "description": "需要执行的数学表达式，例如'(3+2)*5'",
                "type": "str",
                "required": True
            }
        ],
        "return_description": {
            "result": "表达式计算结果"
        }
    },

    "knowledge_retrieval_api":
    {
        "tool": "知识库查询工具",
        "api_name": "knowledge_retrieval_api",
        "api_description": "根据输入的query，查询知识库中相关文档内容。",
        "parameters": [
            {
                "name": "query",
                "description": "用户的提问的规范表达，例如:解释什么是话费透支免单",
                "required": True,
                "type": "str"
            },
            {
                "name": "keyword",
                "description": "用户问题的关键词，例如:话费透支免单",
                "required": True,
                "type": "str"
            }
        ],
        "return_description": {
            "result": "与该问题查到的相关文档内容"
        }
    },

    "get_weather_info_api":
    {
        "tool": "天气查询工具",
        "api_name": "get_weather_info_api",
        "api_description": "查询某个城市今天或未来某天的天气情况，不支持查询过去日期的天气。",
        "parameters": [
            {
                "name": "city",
                "description": "用户需要查询的城市名称列表，如果是空列表，则表示查询本地城市",
                "required": True,
                "type": "List[str]"
            },
            {
                "name": "date",
                "description": "用户需要查询的日期列表，必须是标准时间格式'yyyy-mm-dd'，如果查今天，可直接传入空列表，注意",
                "required": True,
                "type": "List[str]"
            }
        ],
        "return_description": {
            "result": [
                {
                    "city": "查询的城市名称",
                    "date": "查询的日期",
                    "weather": "天气，例如`晴`",
                    "temperatureRange": "气温范围",
                    "minimumTemperature": "最低气温",
                    "maximumTemperature": "最高气温",
                    "airQualityIndex": "空气质量指数",
                    "airQualityLevel": "空气质量等级",
                    "humidity": "湿度",
                    "wind": "风向",
                    "windForce": "风力",
                    "ultraviolet": "紫外线等级",
                    "clothing_suggestion": "衣着建议",
                    "coldIndex": "感冒指数",
                    "trafficIndex": "交通指数",
                    "exerciseIndex": "运动指数",
                    "tourismIndex": "旅游指数"
                }
            ]
        }
    },


    "global_connection_traval_api":
    {
        "tool": "全球通出行工具",
        "api_name": "global_connection_traval_api",
        "api_description": "提供全球通出行相关权益和服务页面跳转操作，全球通出行服务场景包括机场休息室服务、高铁休息室服务、高铁列车餐食服务、旅游礼遇、酒店礼遇、出境礼遇。",
        "parameters": [
            {
                "name": "city",
                "description": "用户提到的全球通出行权益相关的城市，可以是多个地点，当没提到任何地点时，应传入空列表",
                "required": True,
                "type": "List[str]"
            },
            {
                "name": "travel_type",
                "description": "当用户问题涉及机场休息室或高铁休息室时传入该参数，只能是'机场休息室'或'高铁休息室'，严禁传入其他任何内容，可以是二者都包含，例如['机场休息室']或者['机场休息室','高铁休息室']，当没有提到时，应传入空列表",
                "required": True,
                "type": "List[str]"
            }
        ],
        "return_description": {
            "result": "回复用户时的话术模板"
        }
    },

    "global_connection_zone_api":
    {
        "tool": "全球通专区工具",
        "api_name": "global_connection_zone_api",
        "api_description": "提供全球通专区页面跳转展示操作，全球通专区内容包含：全球通品牌活动（全球通星动日活动、逐马计划、全球通蓝色梦想公益计划）、5G直通车活动、全球通尊享服务、全球通尊享特权",
        "parameters": [],
        "return_description": {
            "result": "回复用户时的话术模板"
        }
    },

    "pay_living_expenses_api":
    {
        "tool": "生活缴费充值工具",
        "api_name": "pay_living_expenses_api",
        "api_description": "生活缴费充值接口，包括电费、水费、燃气费和暖气费等充值",
        "parameters": [
            {
                "name": "amount",
                "description": "充值金额",
                "type": "str",
                "required": True
            },
            {
                "name": "type",
                "description": "充值类型，包括['电费','水费','燃气费','暖气费']",
                "type": "str",
                "required": True
            }
        ],
        "return_description": {
            "result": "回复用户时的话术模板"
        }
    },

    "get_living_balance_info_api":
    {
        "tool": "生活缴费余额查询",
        "api_name": "get_living_balance_info_api",
        "api_description": "生活缴费余额查询接口，包括['电费','水费','燃气费','暖气费']",
        "parameters": [
            {
                "name": "type",
                "description": "要查询的缴费类型，当用户未明确查什么余额时填'none'",
                "type": "List[str]",
                "required": True
            }
        ],
        "return_description": {
                "result": [
                    {
                    "type": "电费",
                    "balance": "50.00元"
                    },
                    {
                    "type": "水费",
                    "balance": "39元"
                    },
                    {
                    "type": "燃气费",
                    "balance": "100.00元"
                    }
                ],
                "reminder": "灵犀已为您查到，您当前账户电费余额50元，水费余额39元，燃气费余额100元。建议您及时充值。"
}
    },

    "open_living_expenses_info_api":
    {
        "tool": "生活缴费记录页面跳转工具",
        "api_name": "open_living_expenses_info_api",
        "api_description": "打开生活缴费记录的查询界面，查询电费、水费、燃气费和暖气费",
        "parameters": [],
        "return_description": {
            "result": "回复用户的话术模板"
        }
    },

    "multimedia_content_search_api":
    {
        "tool": "影视、音乐、阅读内容查询工具",
        "api_name": "multimedia_content_search_api",
        "api_description": "根据场景类别（电影/电视剧/音乐/阅读/体育）和关键字（如作品名称/导演/主演/歌手/作者/类型/风格）搜索出相关的具体作品。",
        "parameters": [
            {
                "name": "user_query",
                "description": "用户输入的query，例如'我想看沈腾主演的电影'",
                "type": "str",
                "required": True
            },
            {
                "name": "moduleType",
                "description": "需要查询的媒体类别，仅限于【'movie（表示电影）'、'tv（表示电视剧）'、'music（表示音乐）'、'reading（表示阅读）'、'sport（表示体育赛事）'】，不能是枚举项之外的其他值。输入示例：['movie']",
                "type": "List[str]",
                "required": True
            },
            {
                "name": "keyword",
                "description": "用于搜索的关键词，可以是电影电视剧的名称、导演、主演、类型，或者音乐的歌名、歌手、专辑名，或者书籍的书名、作者、类型；如果提到多项应该输入其中的多项。输入示例：['周星驰', '功夫', '喜剧']",
                "type": "List[str]",
                "required": True
            }
        ],
        "return_description": {
            "result": [
                {
                    "name": "作品名称",
                    "moduleType": "作品类型",
                    "description": "作品简介"
                }
            ],
            "回复话术": "回复用户时的话术模板"
        }
    },

    "multimedia_rank_search_api":
    {
        "tool": "影视、音乐、阅读榜单查询工具",
        "api_name": "multimedia_rank_search_api",
        "api_description": "根据场景类别（电影/电视剧/音乐/阅读/体育）搜索出相应场景榜单上排名靠前的作品。",
        "parameters": [
            {
                "name": "moduleType",
                "description": "需要查询的媒体类别，仅限于【'movie（表示电影）'、'tv（表示电视剧）'、'music（表示音乐）'、'reading（表示阅读）'、'sport（表示体育赛事）'】，如果提到多项应该输入其中的多项，但不能是枚举项之外的其他值。输入示例：['movie', 'tv']",
                "type": "List[str]",
                "required": True
            }
        ],
        "return_description": {
            "result": [
                {
                    "name": "作品名称",
                    "moduleType": "作品类型"
                }
            ],
            "回复话术": "回复用户时的话术模板"
        }
    },

    "movie_ticket_api":
    {
        "tool": "电影购票工具",
        "api_name": "movie_ticket_api",
        "api_description": "在用户想要购买电影票时，根据输入的关键词，返回匹配到的电影详情。",
        "parameters": [
            {
                "name": "keyword",
                "description": "用户提到的关键词，例如电影的电影名、导演、演员、类型、简介等。输入示例：['爱情片', '泰坦尼克']",
                "type": "List[str]",
                "required": True
            },
            {
                "name": "place",
                "description": "用户提到的位置信息，例如城市、地区",
                "type": "str",
                "required": True
            }
        ],
        "return_description": {
            "result": [
                {
                    "name": "电影名称",
                    "description": "电影简介",
                }
            ],
            "回复话术": "回复用户时的话术模板"
        }
    },

    "cinema_find_api":
    {
        "tool": "电影院搜索工具",
        "api_name": "cinema_find_api",
        "api_description": "搜索附近的电影院",
        "parameters": [
            {
            "name": "place",
            "description": "用户提到的位置信息，例如城市、地区",
            "type": "str",
            "required": True
        }
        ],
        "return_description": {
            "result": "是否搜索成功",
            "回复话术": "回复用户时的话术模板"
        }
    },
    "start_living_expenses_info_api":
    {
        "tool": "首页打开工具",
        "api_name": "start_living_expenses_info_api",
        "api_description": "为用户打开生活缴费页面，当用户意图既不是生活缴费充值、也不是生活缴费余额查询、也不是生活缴费记录页面跳转时，才会调用该工具为用户打开首页，该工具只会在第一次才可能被调用，该工具不会在其他工具之后调用。",
        "parameters": [],
        "return_description": {
            "result": "打开首页的回复话术，例如'回复话术：灵犀已为您打开生活缴费页面，您可以在这里进行缴费哦~'"
            }
    },

    "complex_visualization_api":
    {
        "tool": "复杂绘图工具",
        "api_name": "complex_visualization_api",
        "api_description": "可以根据用户提供的数据，绘制图表，并返回完成状态",
        "parameters": [
            {
                "name": "x",
                "description": "横轴数据，例如 {'日期':['2024-01-20', '2024-01-21','2024-01-22']}",
                "type": "Dict",
                "required": True
            },
            {
                "name": "y",
                "description": "纵轴数据，括号为单位，例如 [{'最高气温(摄氏度)':['15', '14', '18']},{'最低气温(摄氏度)':['5', '2', '10']}]",
                "type": "List[Dict]",
                "required": True
            },
            {
                "name": "type",
                "description": "枚举值：折线图、柱状图、饼状图和表格。趋势类的数据选择折线图，对比类数据选择柱状图，详情类数据画饼状图，面板数据选择表格，例如 '折线图'。",
                "type": "str",
                "required": True
            }
        ],
        "return_description": {
                "result": "固定返回'success',表示绘图完成。"
        }
    },

    "retrieve_relocate_contact_api":
    {
        "tool": "检索定位触点工具",
        "api_name": "retrieve_relocate_contact_api",
        "api_description": "根据用户的输入，检索定位用户输入中的触点名称",
        "parameters": [
            {
                "name": "query",
                "description": "用户的输入",
                "required": True,
                "type": "str"
            },
            {
                "name": "keyword",
                "description": "权益触点的名称",
                "required": True,
                "type": "List[str]"
            }
        ],
        "return_description": {
            "result": [
                {
                    "name": "权益触点的名称",
                    "info": "权益触点的简介"
                }
            ]
        }
    },

    "open_contact_api":
    {
        "tool": "打开触点工具",
        "api_name": "open_contact_api",
        "api_description": "打开权益触点的工具API",
        "parameters": [
            {
                "name": "keyword",
                "description": "权益触点的名称",
                "required": True,
                "type": "str"
            }
        ],
        "return_description": {
            "result": {
                "name": "权益触点的名称",
                "info": "权益触点的简介"
            }
        }
    },

    "contact_knowledge_retrieval_api":
        {
        "tool": "触点知识库检索工具",
        "api_name": "contact_knowledge_retrieval_api",
        "api_description": "根据用户的输入，查询知识库中的权益触点信息",
        "parameters": [
            {
                "name": "query",
                "description": "用户的输入",
                "required": True,
                "type": "str"
            },
            {
                "name": "keyword",
                "description": "权益相关的关键词",
                "required": True,
                "type": "List[str]"
            }
        ],
        "return_description": {
            "result": [
                {
                    "name": "权益触点的名称",
                    "info": "权益触点的简介"
                }
            ]
        }
    },

    "work_detail_search_api":
        {
            "tool": "作品详情查询工具",
            "api_name": "work_detail_search_api",
            "api_description": "查询并返回一部或多部作品（电影、电视剧、音乐、书籍、体育）的详情信息。",
            "parameters": [
                {
                    "name": "user_query",
                    "description": "用户问题",
                    "type": "str",
                    "required": True
                },
                {
                    "name": "work_name",
                    "description": "作品名称",
                    "type": "List[str]",
                    "required": True
                },
                {
                    "name": "moduleType",
                    "description": "作品类型，仅限于【'movie（表示电影）'、'tv（表示电视剧）'、'music（表示音乐）'、'reading（表示阅读）'、'sport（表示体育赛事）'】，需要根据上下午对话历史进行判断。",
                    "type": "List[str]",
                    "required": True
                }
            ],
            "return_description": {
                "result": [
                    {
                        "work_name": "作品名称",
                        "work_detail": "作品详情，电影电视剧作品应包含导演、主演、类型、风格、评分、简介等；音乐作品应包含歌名、歌手、专辑名、简介信息等；书籍作品应包含书名、作者、类型、简介信息等等。"
                    }
                ]
            }
        },
    "work_open_api":
        {
            "tool": "作品页面打开工具",
            "api_name": "work_open_api",
            "api_description": "打开并进入某个作品的详情页面",
            "parameters": [
                {
                    "name": "work_name",
                    "description": "需要打开的作品名称",
                    "required": True,
                    "type": "str"
                },
                {
                    "name": "work_index",
                    "description": "需要打开的作品索引，**仅从用户问题中提取**",
                    "required": False,
                    "type": "str"
                },
                {
                    "name": "moduleType",
                    "description": "要打开的作品类型，仅限于【'movie（表示电影）'、'tv（表示电视剧）'、'music（表示音乐）'、'reading（表示阅读）'、'sport（表示体育赛事）'】，需要根据上下午对话历史进行判断。",
                    "type": "str",
                    "required": True
                },
            ],
            "return_description": {
                "result": "'success',表示打开成功"
            }
        },

    "get_detail_bill_cost_in_month_api":
    {
        "tool": "详细账单查询工具",
        "api_name": "get_detail_bill_cost_in_month_api",
        "api_description": "查询用户某个或多个月份的消费账单，返回内容包括当月的总消费金额，扣费项目和具体的扣费明细。",
        "parameters": [
            {
                "name": "year_month",
                "description": "用户需要查询的所有年月，每项必须是一个字典，month和year都必须是阿拉伯数字字符串，例如[{'year':'2024','month':'4'}]",
                "type": "List[Dict]",
                "required": True
            }
        ],
        "return_description": {
            "result": [
                {
                    "year_month": "查询结果所属年月",
                    "total_bill": "总消费金额",
                    "save_bill": "优惠金额",
                    "actual_pay": "实际应付金额",
                    "套餐及固定费用": {
                        "total_money": "套餐及固定费用总金额",
                        "details": "套餐及固定费用明细"
                    },
                    "增值业务费用": {
                        "total_money": "增值业务费用总金额",
                        "details": "套增值业务费用明细"
                    },
                    "套餐外费用": {
                        "total_money": "套餐外费用总金额",
                        "details": "套餐外费用明细"
                    },
                    "代收费用": {
                        "total_money": "代收费总金额",
                        "details": "代收费明细"
                    },
                    "其他费用": {
                        "total_money": "其他费用总金额",
                        "details": "其他费用明细"
                    }
                }
            ],
            "提醒事项": "回答用户时，需要提醒用户的注意事项，例如是否产生超套消费等。"
        }
    },

    "open_point_product_info_api":
    {
        "tool": "自动跳转积分商品详情页面工具",
        "api_name": "open_point_product_info_api",
        "api_description": "根据用户需要查询的某个积分商品，自动跳转积分商品详情页面",
        "parameters": [
            {
                "name": "product_id",
                "description": "积分商品的id",
                "type": "str",
                "required": False
            },
            {
                "name": "product_name",
                "description": "积分商品的名称",
                "type": "str",
                "required": True
            }
        ],
        "return_description": {
            "result": [
                {
                    "product_id": "积分商品的ID",
                    "product_name": "积分商品的名称",
                    "point_cost": "兑换积分商品所需的积分",
                    "price_cost": "积分商品的价格",
                    "product_info": "积分商品的具体信息",
                    "is_open": "返回积分商品跳转状态，例如 'success' "
                }
            ]
        }
    },

    "get_point_product_info_api":
    {
        "tool": "积分商品信息查询工具",
        "api_name": "get_point_product_info_api",
        "api_description": "查询积分商品的具体信息，支持查询多个积分商品信息。",
        "parameters": [
            {
                "name": "product",
                "description": "积分商品的信息，包括积分商品的id和名称",
                "type": "List[Dict]",
                "required": False
            },
            {
                "name": "query",
                "description": "用户查询积分商品信息的Question",
                "type": "str",
                "required": True
            }
        ],
        "return_description": {
            "result": [
                {
                    "product_id": "积分商品的ID",
                    "product_name": "积分商品的名称",
                    "point_cost": "兑换积分商品所需的积分",
                    "price_cost": "积分商品的价格",
                    "product_info": "积分商品的具体信息"
                }
            ]
        }
    },

    "recommend_point_product_api":
    {
        "tool": "积分商品推荐工具",
        "api_name": "recommend_point_product_api",
        "api_description": "用户积分可兑换的商品推荐",
        "parameters": [
            {
                "name": "point_range",
                "description": "积分商品所需的积分范围",
                "type": "List",
                "required": False
            },
            {
                "name": "price_range",
                "description": "积分商品的价格范围",
                "type": "List",
                "required": False
            },
            {
                "name": "product_type",
                "description": "积分商品的类型",
                "type": "List",
                "required": False
            },
            {
                "name": "keywords",
                "description": "积分商品的关键字",
                "type": "List",
                "required": False
            }
        ],
        "return_description": {
            "result": [
                {
                    "product_id": "积分商品的ID",
                    "product_name": "积分商品的名称",
                    "product_type": "积分商品的类型",
                    "point_cost": "兑换积分商品所需的积分",
                    "price_cost": "积分商品的价格",
                    "product_description": "积分商品的简介"
                }
            ]
        }
    },

    "get_plan_balance_info_api":
    {
        "tool": "套餐余量查询工具",
        "api_name": "get_plan_balance_info_api",
        "api_description": "查询用户本月的免费资源（流量，短信和语音(包含语音和视频通话)）的总量、使用量和余量信息。",
        "parameters": [],
        "return_description": {
            "result": {
                "flow": "流量的总量、使用量和余量信息",
                "message": "短信的总量、使用量和余量信息",
                "voice": "语音的总量、使用量和余量信息"
            }
        }
    },

    "main_plan_detail_api":
    {
        "tool": "主套餐详情查询工具",
        "api_name": "main_plan_detail_api",
        "api_description": "用于查询用户当前主套餐的详情信息。",
        "parameters": [],
        "return_description": {
            "result":
                {
                    "curPlanName": "当前主套餐名称",
                    "busiInfomsg": "主套餐详情",
                    "startTime": "当前主套餐生效时间",
                    "endTime": "当前主套餐结束时间",
                    "planPrice": "主套餐的资费档位，单位元",
                    "busiInfoList（当前主套餐下主要资费信息）": [
                        {
                            "busiName":"资费名称",
                            "busiNum":"资源总量（包含单位）",
                            "busiprice":"资费价格，单位元",
                            "gatFlag":"是否包含港澳台标识",
                            "type":"资费类型，包括：全国通用流量、定向流量、语音、短信、其他",
                        }
                    ],
                    "planFlag": "套餐类型，包括：5G套餐、4G套餐、其他套餐",
                    "subNumber": "副卡号码"
                }
        }
    },

    "get_consumer_info_api":
    {
        "tool": "用户信息查询工具",
        "api_name": "get_consumer_info_api",
        "api_description": "查询用户手机号、地区、入网时间、网龄、信用分和星级等信息。",
        "parameters": [],
        "return_description": {
            "result": [
                {
                    "phoneNumber": "用户手机号",
                    "province": "用户所在省份",
                    "networkAccessDate": "用户入网时间",
                    "internetAge": "用户的网龄",
                    "creditScore": "用户信用分",
                    "starLevel": "用户星级"
                }
            ]
        }
    },
    # 钱奎
    "get_menu_match_api":
        {
            "tool": "菜单匹配查询",
            "api_name": "get_menu_match_api",
            "api_description": "根据输入的query，查询获取匹配的相关菜单。当用户表达要打开/看/了解/办理/查/熟悉/确认等一个看起来是个应用，产品或者套餐的时候需要调用。返回结果为：state为调用状态;log为日志记录，可以存放没有菜单或没有权限;info为具体的菜单结果。",
            "parameters": [{
                "name": "query",
                "description": "用户的提问的规范表达，例如:缴纳话费的入口",
                "required": True,
                "type": "str"
            }, {
                "name": "keyword",
                "description": "用户问题的关键词，例如:缴纳话费",
                "required": True,
                "type": "str"
            }],
            "return_description": {
                "result": {
                    "state": "success",
                    "log": "成功执行",
                    "info": [{
                        "name": "菜单1",
                        "id": "id1"
                    }, {
                        "name": "菜单2",
                        "id": "id2"
                    }]
                }
            }
        },

    "get_knowledge_business_api":
        {
            "tool": "业务知识库查询",
            "api_name": "get_knowledge_business_api",
            "api_description": "根据输入的query，查询知识库中相关文档内容。当用户表达看下/查看/查等 想了解某个应用，产品，套餐的具体知识的时候需要调用，重点是说话的目标是具体的知识。返回结果为：state为调用状态;log为日志记录，可以存放没有文档或没有权限;info为具体的文档结果。",
            "parameters": [{
                "name": "query",
                "description": "用户的提问的规范表达，例如:守机宝的最低资费是多少",
                "required": True,
                "type": "str"
            }, {
                "name": "keyword",
                "description": "用户问题的关键词，例如:守机宝",
                "required": True,
                "type": "str"
            }],
            "return_description": {
                "result": {
                    "state": "success",
                    "log": "成功执行",
                    "info": [{
                        "name": "文档名称1",
                        "info": {"段落1": "***", "段落2": "***"},
                        "type": "菜单文档"
                    }, {
                        "name": "文档名称2",
                        "info": {"段落1": "***", "段落2": "***"},
                        "type": "补充文档"
                    }]
                }
            }
        },

    "open_menu_show_api":
        {
            "tool": "菜单页面跳转",
            "api_name": "open_menu_show_api",
            "api_description": "打开对应的菜单页面，返回状态结果和日志内容。",
            "parameters": [{
                "name": "menu_name",
                "description": "需要打开的菜单名称",
                "type": "str",
                "required": True
            }, {
                "name": "menu_id",
                "description": "需要打开的菜单ID",
                "type": "str",
                "required": True
            }],
            "return_description": {
                "result": {
                    "state": "sucess",
                    "log": "成功打开"
                }
            }
        },

    "chat_normal_api":
        {
            "tool": "闲聊回答",
            "api_name": "chat_normal_api",
            "api_description": "当用户闲聊时，不要擅自回答，调用此工具获取闲聊的回复。",
            "parameters": [{
                "name": "query",
                "description": "用户闲聊的原始问题，例如:你知道飞机有几个翅膀吗",
                "required": True,
                "type": "str"
            }],
            "return_description": {
                "result": "回复用户的话术模板"
            }
        },

    "work_clock_api":
        {
            "tool": "上下班打卡",
            "api_name": "work_clock_api",
            "api_description": "触发打卡功能，打卡方式分上班打卡和下班打卡。返回state结果和log内容。",
            "parameters": [{
                "name": "clock_type",
                "description": "打卡方式",
                "type": "str",
                "required": True
            }],
            "return_description": {
                "result": {
                    "state": "sucess",
                    "log": "成功打开"
                }
            }
    }

}

