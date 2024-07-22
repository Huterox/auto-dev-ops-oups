"""
@FileName：__init__.py
@Author：Huterox
@Description：Go For It
@Time：2024/6/30 19:10
@Copyright：©2018-2024 awesome!
"""
import os

from base import mylogger

current_directory = os.getcwd()
entries = os.listdir(current_directory)
folders = [entry for entry in entries if os.path.isdir(os.path.join(current_directory, entry))]
for folder in folders:
    mylogger.info(f"已检测到本地Whisper模型{folder}")