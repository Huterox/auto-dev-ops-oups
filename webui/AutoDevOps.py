"""
@FileName：AutoDevOps.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/20 15:44
@Copyright：©2018-2024 awesome!
"""
import streamlit as st
import streamlit_antd_components as sac

from workflow.templates import TEMPLATES, SHOW_FLOW_TEMPLATE


def autoUI():
    sac.alert(label='Tips',
              description=f'在当前页面可查看当前系统具备的工作流，并进行选定查看，在当前页面选定后，即可在自动生成页面执行触发对应工作流',
              size=12,
              color='success',
              banner=False,
              icon=True, closable=True)
    # 流程查看
    select_flow = sac.segmented(
        items=[
            sac.SegmentedItem(label=flow["name"],icon=flow["icon"]) for flow in TEMPLATES
        ],
    )
    st.session_state.select_flow = select_flow

    show_flow_graph = st.container(height=400)
    with show_flow_graph:
        SHOW_FLOW_TEMPLATE.get(select_flow)()



