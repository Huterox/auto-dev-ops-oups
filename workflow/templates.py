"""
@FileName：templates.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/27 20:54
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.chat import chat_flow
from workflow.build_system.graph import graph_show_with_st

"""
工作流模板，当前主要展示支持的工作流模板，不过目前在当前节段也只是有一个模板
注意每个模板对应一个Python工程包，工程包需要具备独立运行的能力，当前系统只是提供可视化操作用户界面
每个工程包具备以下基本要求：
1. 指定可视化模块
2. 执行流主入口
3. 状态管理器，如果不独立实现，默认使用streamlit状态管理
"""

TEMPLATES = [
    {
        "name":"PYTHON WEB SYSTEM GENERATED🥴",
         "icon":"share-fill",
    }
]

BUILD_FLOW_TEMPLATE = {
    "PYTHON WEB SYSTEM GENERATED🥴":None
}

SHOW_FLOW_TEMPLATE = {
    "PYTHON WEB SYSTEM GENERATED🥴":graph_show_with_st
}

CHAT_FLOW_TEMPLATE = {
    "PYTHON WEB SYSTEM GENERATED🥴": chat_flow
}