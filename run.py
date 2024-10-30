# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : run.py
# Time       ：2024/6/15 06:04
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from app import create_app
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("--port", type=int, default=9100, help="port")
args, unknown_args = parser.parse_known_args()







if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,host="0.0.0.0", port=args.port)

