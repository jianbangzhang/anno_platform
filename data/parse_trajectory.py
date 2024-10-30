# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : parse_trajectory.py
# Time       ：2024/5/18 10:17
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from utils.data_utils import parse_tracjectory


def parse_chat_text(text):
    text = text.strip()
    text_lst = [line.strip() for line in text.split("\n") if line.strip()]

    size = len(text_lst)

    i = 0
    block_lst = []
    round=0
    while i < size and round<size:
        cur_line = text_lst[i]
        cur_line=cur_line.replace("：",":")
        if i + 1 == size:
            break
        next_line = text_lst[i + 1]
        round+=1
        if cur_line.startswith("Question") and next_line.startswith("Thought"):
            question=cur_line
            start_id = i
            flag = False
            for j in range(i + 1, size):
                choose_line = text_lst[j]
                if choose_line.startswith("Finish") and not flag:
                    end_id = j
                    block_text = text_lst[start_id+1:end_id + 1]
                    block_text=[line for line in block_text if line]
                    block_text="\n".join(block_text)
                    block_text,code=parse_tracjectory(block_text,is_replace=False)
                    if code==-1:
                        pass
                    else:
                        block_lst.append([question,block_text])

                    flag = True
                    i = end_id
                else:
                    continue
        else:
            i += 1

    if block_lst:
        code=0
    else:
        code=-1

    return block_lst,code




def parse_input_text(text_lst):
    """
    :param text_lst:
    :return:
    """
    size = len(text_lst)
    i = 0
    block_lst = []
    try:
        while i < size:
            cur_line = text_lst[i]
            if cur_line.startswith("Question") and i==size-1:
                if not (len(block_lst) > 0 and cur_line == block_lst[0]):
                    cur_line="<User> "+cur_line.replace("Question:","").strip()+"<end><Bot>"
                    block_lst.append(cur_line)

            if cur_line.startswith("Observation"):
                block_lst.append(cur_line)
                i+=1
                continue

            if i + 1 == size:
                break
            next_line = text_lst[i + 1]
            if cur_line.startswith("Question") and next_line.startswith("Thought"):
                if not (len(block_lst) > 0 and cur_line == block_lst[0]):
                    cur_line = "<User> " + cur_line.replace("Question:", "").strip()
                    block_lst.append(cur_line)

                start_id = i
                flag = False
                for j in range(i + 1, size):
                    choose_line = text_lst[j]
                    if choose_line.startswith("Action_Parameter") and not flag:
                        end_id = j
                        block_text = text_lst[start_id+1:end_id + 1]
                        block_text = [line for line in block_text if line]
                        block_text ="<Bot>"+"\n".join(block_text)
                        block_lst.append(block_text)
                        flag = True
                        i = end_id+1
                    else:
                        continue

                if not flag:
                    i+=1
            elif cur_line.startswith("Thought") and next_line.startswith("Action"):
                start_id = i
                flag = False
                thought=cur_line
                for j in range(i + 1, size):
                    choose_line = text_lst[j]
                    if choose_line.startswith("Action_Parameter") and not flag:
                        end_id = j
                        block_text = text_lst[start_id+1:end_id + 1]
                        block_text = [line for line in block_text if line]
                        block_text = thought+"\n".join(block_text)
                        block_lst.append(block_text)
                        flag = True
                        i = end_id + 1
                    else:
                        continue

                if not flag:
                    i+=1
            elif cur_line.startswith("Thought") and next_line.startswith("Finish"):
                block_text = cur_line+"\n"+next_line
                block_lst.append(block_text)
                i+=2
            else:
                i+=1
    except:
        code=-1
        return block_lst, code

    if block_lst:
        code = 0
    else:
        code = -1
    return block_lst, code