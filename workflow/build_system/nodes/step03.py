"""
@FileName：step01.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/5 21:26
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.agents.step03 import AgentStep3
from workflow.build_system.nodes.node import FlowNode
from workflow.build_system.nodes.variables import FlowVariables
from workflow.build_system.system_state import CHAT_FLOW_STATE
import streamlit_antd_components as sac
import streamlit as st
import time

class FlowNodeStep3(FlowNode):

    def __init__(self, name):
        self.agent = AgentStep3()
        self.flow_node_name = name
        self.index = 2
        self.values = FlowVariables("step03")

    def described_show(self):
        info = """
        当前节点为第二个节点主要负责数据库建模🚓
        """
        sac.alert(label='节点描述',
                  description=info,
                  size=12,
                  banner=[False, True],
                  color='indigo',
                  icon=False,
                  variant='transparent',
                  closable=True)

    @st.experimental_dialog('变量')
    def variable_show(self):
        st.text_area(label="变量值",
                     value=self.values.get(),
                     key="variable_show_step_3",
                     height=300
                     )
        self.values.set(st.session_state.get("variable_show_step_3"))

    def get_index(self):
        return self.index

    def message_show(self, flow_chat_messages):
        if not CHAT_FLOW_STATE.get_state("messages_step_3"):
            CHAT_FLOW_STATE.set_state("messages_step_3",
                                      [
                                          {"role": "assistant", "content": "你好我是当前工作流的对话助手小C🌎"}
                                      ]
                                      )
            # 项目助手对话的记录
        for msg in CHAT_FLOW_STATE.get_state("messages_step_3"):
            flow_chat_messages.chat_message(msg["role"]).write(msg["content"])

    def get_res(self, input_prompt: str, st, flow_chat_messages):

        # 显示用户的输入
        flow_chat_messages.chat_message("user").write(input_prompt)
        # 拿到结果
        histroy = CHAT_FLOW_STATE.get_state("messages_step_3")
        # get_res 会将用户的输入和返回的结果都放在histroy里面的
        msg = self.agent.get_res(histroy, input_prompt)
        # 这里需要将变量写进去
        self.values.set(msg)
        # 将记录写进去
        CHAT_FLOW_STATE.set_state("messages_step_3", histroy)

        with flow_chat_messages.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ''
            for item in msg:
                full_response += item
                time.sleep(0.01)
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
            # 在这里提供切换当前bot的选项
            r_001, r_002 = st.columns([0.6, 0.4])
            with r_001:
                st.markdown("😊")
            with r_002:
                if st.button("03下一步", type="primary"):
                    self.next_flow_node()

    def next_flow_node(self):
        # 记录一下，当前的节点执行完毕
        # 如果需要切换上一个节点，那么你要找到上一个节点的上一个节点才能完成切换
        # 如果切换当前节点，则需要上一个节点
        # 如果切换下一个节点，这设置当前节点 对于 current_flow_node_done 的值
        # 当前批次的工作流，还没有涉及到节点切换
        CHAT_FLOW_STATE.set_state("current_flow_node_done", self.flow_node_name)
