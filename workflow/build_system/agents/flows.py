"""
@FileName：flows.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/4 14:17
@Copyright：©2018-2024 awesome!
"""
import time

from workflow.build_system.agents.agents import FlowAgent, AgentStep1
from workflow.build_system.agents.variables import FlowVariables
from workflow.build_system.system_state import CHAT_FLOW_STATE

"""
工作流节点，负责管理整个工作流的节点
对Agent进行封装，除了需要实现具体的prompt和tools的调用之外（RAG本质上也就是Tools的调用）
还需要做如下事情：
1. 提供分支切换函数，同时完成分支切换
2. 按照要求流程将变量值设置在变量当中，便于其Agent调用

TODO: 现在暂时没有可视化创作界面，因此没有办法通过JSON模板去生成这样的FlowNode只能先进行编码
"""
import streamlit as st
import streamlit_antd_components as sac

class FlowNode(object):

    def get_index(self):
        pass

    def message_show(self, flow_chat_messages):
        pass

    def get_res(self, input_prompt: str, st, flow_chat_messages):
        pass

    @st.experimental_dialog('变量')
    def variable_show(self):
        pass

    def described_show(self):
        pass


class FlowNodeStep1(FlowNode):

    def __init__(self):
        self.agent = AgentStep1()
        self.next_node = None
        self.last_node = None
        self.index=0
        # 注意当前不同的FlowNodeStep其实可能会有多个变量，但是现在还没有提取模板
        # 所以的话，就先这样设计，我们会提供一个展示变量的函数，对其进行实现就好了
        self.values = FlowVariables("step01")

    def described_show(self):
        info = """
        当前节点为第一个节点主要负责提取需求🚓
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
                     key="variable_show_step_1",
                     height=300
                     )
        self.values.set(st.session_state.get("variable_show_step_1"))


    def get_index(self):
        return self.index


    def message_show(self,flow_chat_messages):
        if not CHAT_FLOW_STATE.get_state("messages_step_1"):
            CHAT_FLOW_STATE.set_state("messages_step_1",
                                      [
                                          {"role": "assistant", "content": "你好我是当前工作流的对话助手🌎"}
                                      ]
                                      )
            # 项目助手对话的记录
        for msg in CHAT_FLOW_STATE.get_state("messages_step_1"):
            flow_chat_messages.chat_message(msg["role"]).write(msg["content"])



    def get_res(self,input_prompt:str,st,flow_chat_messages):

        # 显示用户的输入
        flow_chat_messages.chat_message("user").write(input_prompt)
        # 拿到结果
        histroy = CHAT_FLOW_STATE.get_state("messages_step_1")
        # get_res 会将用户的输入和返回的结果都放在histroy里面的
        msg = self.agent.get_res(histroy,input_prompt)
        # 这里需要将变量写进去
        self.values.set(msg)
        # 将记录写进去
        CHAT_FLOW_STATE.set_state("messages_step_1", histroy)

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
                st.button("下一步", on_click=None, type="primary")



flow_step01 = FlowNodeStep1()

class FlowNodeManger(object):
    # 这个FlowNodeManger的实现机制本质上其实就是通过system_state来进行处理的
    @staticmethod
    def getFlowNode()->FlowNode:
        # 如果当前状态里面没有FlowNode那么我们默认就将Step1给拿到作为当前的工作流
        flow_node = CHAT_FLOW_STATE.get_state("current_flow_node")
        if flow_node is None:
            flow_node = flow_step01
            CHAT_FLOW_STATE.set_state("current_flow_node",flow_node)
        return flow_node