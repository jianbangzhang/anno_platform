# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : config.py
# Time       ：2024/6/15 11:00
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
import os

class Config:
    MAX_CONTENT_LENGTH = 30 * 1024 * 1024
    DEFAULT_FILE="datasets/example_files/example_agent-split.xlsx"
    DEFAULT_FILE_JSON = "datasets/example_files/example_agent-split.json"
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    PROJECT_DIR = os.path.dirname(current_directory)
    SESSION_FILE_DIR = os.path.join(PROJECT_DIR, 'sessions')
    SESSION_PERMANENT = False
    SECRET_KEY = 'your_secret_key'
    SESSION_TYPE = 'filesystem'

