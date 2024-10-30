# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : userSession.py
# Time       ：2024/7/5 19:42
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
import os
from multiprocessing import Process
from .config import Config

DEFAULT_FILE = Config.DEFAULT_FILE
DEFAULT_FILE_JSON = Config.DEFAULT_FILE_JSON
project_dir=Config.PROJECT_DIR

user_sessions = {}

class UserSystem:
    def __init__(self):
        self.processes = {}

    def create_user_session(self, username):
        if username not in user_sessions:
            user_sessions[username] = {
                'user_name': username,
                'user_folder': os.path.join(project_dir,'datasets', 'user_uploads', username),
                'user_excel_dir': os.path.join(project_dir,'datasets', 'user_uploads', username, "excel_files"),
                'user_json_dir': os.path.join(project_dir,'datasets', 'user_uploads', username, "json_files"),
                'total': 0,
                'anno': 0,
                'user_xlsx_file': DEFAULT_FILE,
                'user_json_file': DEFAULT_FILE_JSON,
                'user_data': []
            }
            user_process = Process(target=run_user_session, args=(username,))
            user_process.start()
            self.processes[username] = user_process
            print(f"Created session for {username}")

    def get_user_session(self, username):
        return user_sessions.get(username, None)

    def stop_user_session(self, username):
        if username in self.processes:
            self.processes[username].terminate()
            self.processes[username].join()
            del self.processes[username]
            del user_sessions[username]
            print(f"Stopped session for {username}")

def run_user_session(username):
    session = user_sessions.get(username, None)
    if session:
        print(f"Running session for {username}")