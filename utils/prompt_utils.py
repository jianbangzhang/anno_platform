# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : prompt_utils.py
# Time       ：2024/5/18 10:32
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""


single_splitter="\n"
double_splitter="\n\n"
splitter_token="<ret>"
double_splitter_token="<ret><ret>"
end_token="<end>"

system_token="<System>"
system="你是中国移动AI智能助理灵犀，能够为用户提供准确、详细的业务咨询和办理服务。"


available_tool_string="""##插件工具集
在回答用户的问题时，可以选择使用给你的工具去调用外部信息进行用户的回复，你可以使用的工具有："""

plan_requirements="""## 输出格式
Thought: 对于已有信息进行整合，并思考接下来应该做什么。
Action: 将要采取的行动。
Action_Parameter: 使用的工具API的输入参数。
Observation: 采取行动后得到的结果，也就是调用现有的工具得到的返回结果。
...（注意以上Thought/Action/Action_Parameter/Observation这个过程必须按顺序进行，并且可以重复进行多轮。）
Thought: 已经获取到所需信息，可以进行对问题的回答。
Finish: 对问题的最终回答，需要对上述过程中的所有信息进行总结后生成回复。"""

question_format=lambda question:f"""接下来开始对话：
<end><User> {question}<end><Bot> """
