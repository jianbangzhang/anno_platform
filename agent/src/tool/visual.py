# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : calendar.py
# Time       ：2024/3/29 15:06
# Author     ：jianbang
# version    ：python 3.10
# company    : IFLYTEK Co.,Ltd.
# emil       : whdx072018@foxmail.com
# Description：
"""
from .base import BaseTool
from agent.utils import retry
import json
import webbrowser
from typing import Tuple




class VisualTool(BaseTool):
    name = "visualization_api"
    is_remote=False
    description="这是一个画图工具"

    def __call__(self, *args, **kwargs)->Tuple:
        date_dict,code=self._call_actual_api()
        return date_dict,code

    @retry(max_retry=1, delay=0)
    def _call_actual_api(self,*args,**kwargs):
        # html = self._generate_chart_html(x, y, labels)
        # with open("chart.html", "w") as f:
        #     f.write(html)

        # webbrowser.open("chart.html")
        return {"result": "success"}




    def _generate_chart_html(self,x, y, labels):
        df = [{"x": xi, "y": yi} for xi, yi in zip(x, y)]

        chart = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "width": 800,
            "height": 400,
            "title": "月度超额数据费用",
            "data": {"values": df},
            "mark": "bar",
            "encoding": {
                "x": {"field": "x", "type": "ordinal", "title": labels['x']},
                "y": {"field": "y", "type": "quantitative", "title": labels['y']},
                "tooltip": [{"field": "x", "type": "ordinal", "title": labels['x']},
                            {"field": "y", "type": "quantitative", "title": labels['y']}]
            }
        }

        chart_json = json.dumps(chart)

        html = f"""
        <!DOCTYPE html>
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>月度超额数据费用</title>
            <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
            <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
            <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }}
                #vis {{
                    margin: 20px auto;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div id="vis"></div>

            <script>
                var chartSpec = {chart_json};

                vegaEmbed("#vis", chartSpec);
            </script>
        </body>
        </html>
        """

        return html



