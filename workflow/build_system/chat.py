"""
@FileName：chat.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/3 14:25
@Copyright：©2018-2024 awesome!
"""
import os
import streamlit as st
import streamlit_antd_components as sac
import toml
from base import current_dir_root

from workflow.build_system.flows import FlowNodeManger



def chat_flow():

    config = toml.load(os.path.join(current_dir_root, "api.toml"))
    sac.alert(label='Tips',
              description=f'欢迎来到系统生成页面，当前流程：PYTHON WEB SYSTEM GENERATED🥴',
              size=12,
              color='success',
              banner=False,
              icon=True, closable=True)

    chat_c0,chat_c1 = st.columns([3,1])

    # 开启对话工作流，聊天助手
    with chat_c0:
        flow_chat_messages = st.container(height=470)
        # 拿到LLM相关的设置
        default_base = config["DEFAULT"]["default_base"]
        default_model = config["DEFAULT"]["default_model"]
        flowNode = FlowNodeManger.getFlowNode()
        # 这里展示当前工作流节点的消息
        flowNode.message_show(flow_chat_messages)
        if (default_base != None and default_model != ""):
            placeholder = "点击Enter开启🐟？😀"
        else:
            placeholder = "有什么我可以帮你的么？😀(请先设置默认大模型KEY)"

        if prompt := st.chat_input(placeholder=placeholder):
            flowNode.get_res(prompt,st,flow_chat_messages)


    # 这里还是展示生成的代码结果
    with chat_c1:
        st.write("")
        flow_state_res = st.container(height=470)
        map_step = {
            "0":sac.StepsItem(title='step 1'),
            "1":sac.StepsItem(title='step 2'),
            "2":sac.StepsItem(title='step 3'),
            "3":sac.StepsItem(title='step 4'),
            "4":sac.StepsItem(title='step 5'),
        }
        with flow_state_res:
            bt = sac.buttons([
                sac.ButtonsItem(label='Describe', color='#4682b4'),
                sac.ButtonsItem(label='Variable', color='#25C3B0'),
            ], label='👀', align='center', variant='filled', color='teal', use_container_width=True)


            if bt == "Describe":
                flowNode.described_show()
            elif bt == "Variable":
                flowNode.variable_show()

            sac.steps(
                items=[
                    step for step in map_step.values()
                ], color='blue', direction='vertical',
                index=flowNode.get_index()
            )



