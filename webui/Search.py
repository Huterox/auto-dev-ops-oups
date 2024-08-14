# -*- coding: utf-8 -*-
# @文件：Search.py
# @时间：2024/8/14 9:44
# @作者：Huterox
# @邮箱：3139541502@qq.com
# -------------------------------

import streamlit as st
import streamlit_antd_components as sac
def searchUI():
    sac.alert(label='Tips',
              description='🎲🎰🕹🔮🧿🎲🔮🧩🧩🧸',
              color='teal',
              banner=False,
              icon=True, closable=True)
    """
    基于MindSearch工作原理，实现动态决策搜索
    1. 自主决策工作链路
    2. 多角色分析搜索结果，决定搜索走向
    3. 并行处理实现
    4. 可视化搜索过程展示
    """

