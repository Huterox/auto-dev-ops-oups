"""
@FileName：ChatFlow.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/3 14:27
@Copyright：©2018-2024 awesome!
"""
import streamlit as st
import streamlit_antd_components as sac

from workflow.templates import CHAT_FLOW_TEMPLATE


def chatFlowUI():
    select_flow = st.session_state.get("select_flow")
    if not select_flow:
        sac.alert(label='Tips',
                  description=f'请前往Auto流程页面，进行选定查看当前系统流程，选定后可回到本页面查看具体的页面',
                  size=12,
                  color='success',
                  banner=False,
                  icon=True, closable=True)
    else:
        CHAT_FLOW_TEMPLATE.get(select_flow)()