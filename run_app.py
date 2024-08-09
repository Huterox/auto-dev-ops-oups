"""
@FileName：run_app.py.py
@Author：Huterox
@Description：Go For It
@Time：2024/6/11 11:42
@Copyright：©2018-2024 awesome!
"""


import os
import sys
from base import run_app
import streamlit.web.cli as stcli

def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path

def run_app_path():
    os.makedirs(run_app,exist_ok=True)
    out = f"{run_app}/main.py"
    return out

if __name__ == "__main__":

    # sys.argv = [
    #     "streamlit",
    #     "run",
    #     resolve_path("main.py"),
    #     "--global.developmentMode=false",
    # ]
    sys.argv = [
        "streamlit",
        "run",
        run_app_path(),
        "--server.port=8080",
        "--global.developmentMode=false",
    ]


    sys.exit(stcli.main())