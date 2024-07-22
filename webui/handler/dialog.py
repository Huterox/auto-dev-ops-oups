"""
@FileName：dialog.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/20 23:28
@Copyright：©2018-2024 awesome!
"""
import streamlit as st
import streamlit_antd_components as sac
@st.experimental_dialog('提示')
def dialog_info(info):
    sac.alert(label='label',
              description=info,
              variant='filled',
              icon=True, closable=True)