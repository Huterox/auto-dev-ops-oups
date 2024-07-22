"""
@FileName：Home.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/20 15:35
@Copyright：©2018-2024 awesome!
"""
import os
import streamlit as st
import streamlit_antd_components as sac
import toml
from base import docs_dir_root, current_dir_root
from webui.handler.homeHandler import home_assistant, load_config_in_state, save_config_in_state, home_settings


def homeUI():
    st.subheader("MathAI V0.1")
    st.caption("POWERED BY @Huterox")


    option_doc_dir = os.path.join(docs_dir_root,"Options.md")
    # 读取到当前项目相关的介绍,方便回答项目相关的细节
    with open(option_doc_dir, 'r', encoding='utf-8') as file:
        doc = file.read()
    select = sac.tabs([
        sac.TabsItem(label='助手', icon='robot'),
        sac.TabsItem(label='设置', icon='gear')
    ], align='center', variant='outline', use_container_width=True, index=0)

    # *******************助手和设置部分***************************
    config = toml.load(os.path.join(current_dir_root, "api.toml"))
    if select == "助手":
        home_assistant(st, doc, config)
    if select == "设置":
        """
        加载配置，并且将其保存在st的session当中
        """
        home_settings(st,config)
        sac.divider(label='POWERED BY @Huterox', icon="lightning-charge", align='center', color='gray', key="5")
