"""
@FileName：step01.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/5 21:26
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.agents.step02 import AgentStep2
from workflow.build_system.nodes.node import FlowNode
from workflow.build_system.variables import FlowVariables
from workflow.build_system.system_state import CHAT_FLOW_STATE
import streamlit_antd_components as sac
import streamlit as st
import time

class FlowNodeStep2(FlowNode):

    def __init__(self, name):
        self.agent = AgentStep2()
        self.flow_node_name = name
        self.index = 1
        self.values = FlowVariables("step02")

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

    @st.dialog('变量',width="large")
    def variable_show(self):
        variable_show_step_2 = st.container(height=400)
        variable_show_step_2.chat_message("assistant").write(self.values.get())

    def get_index(self):
        return self.index


    def init_auto_func(self,flow_chat_messages):

        # 如果说当前没有设置的变量，那么就说明我们当前这个执行节点还是处于初始化的状态
        v = self.values.get()
        time.sleep(1)
        if not v:
            input_prompt = "根据你已知的：RequirementsContent 开始数据库建模"
            with flow_chat_messages.chat_message("assistant"):
                self.printer_show("正在分析您的需求... 接下来要开始发力了!!✨💦")

            with flow_chat_messages.chat_message("assistant"):
                with st.spinner("正在初始化数据库建模......"):
                    histroy = CHAT_FLOW_STATE.get_state("messages_step_2")
                    msg = self.agent.get_res(histroy, input_prompt)
                    # 这里需要将变量写进去  （当前只是确定需求，还可以这样处理没有问题）
                    self.values.set(msg)
                    # 将记录写进去(是的，这里也是需要将变量写进去的，不然下次就会继续触发这个玩意)
                    # 当前的这个用户输出还是要去掉的
                    CHAT_FLOW_STATE.set_state("messages_step_2", histroy)
                    placeholder = st.empty()
                    full_response = ''
                    for item in msg:
                        full_response += item
                        time.sleep(0.002)
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)


    def message_show(self, flow_chat_messages):
        if not CHAT_FLOW_STATE.get_state("messages_step_2"):
            CHAT_FLOW_STATE.set_state("messages_step_2",
                                      [
                                          {"role": "assistant", "content": "你好我是当前工作流的对话助手小B🔅负责数据库建模"}
                                      ]
                                      )
        for msg in CHAT_FLOW_STATE.get_state("messages_step_2"):
            flow_chat_messages.chat_message(msg["role"]).write(msg["content"])

        # 如果触发状态为这个，那么说明当前首次进入当前的节点，按照我们对流程的设计，在这里我们需要先进行初始化处理
        self.init_auto_func(flow_chat_messages)

        with flow_chat_messages:
            r_001, r_002 = st.columns([0.6, 0.4])
            with r_001:
                st.markdown("💨")
            with r_002:
                st.button("next02", on_click=self.next_flow_node, args=(flow_chat_messages,))

    def get_res(self, input_prompt: str, st, flow_chat_messages):

        # 显示用户的输入
        flow_chat_messages.chat_message("user").write(input_prompt)
        # 拿到结果
        histroy = CHAT_FLOW_STATE.get_state("messages_step_2")
        # get_res 会将用户的输入和返回的结果都放在histroy里面的
        msg = self.agent.get_res(histroy, input_prompt)
        # 这里需要将变量写进去  （当前只是确定需求，还可以这样处理没有问题）
        self.values.set(msg)
        # 将记录写进去
        CHAT_FLOW_STATE.set_state("messages_step_2", histroy)

        with flow_chat_messages.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ''
            for item in msg:
                full_response += item
                time.sleep(0.002)
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)


    def next_flow_node(self,flow_chat_messages):
        # 记录一下，当前的节点执行完毕
        # 如果需要切换上一个节点，那么你要找到上一个节点的上一个节点才能完成切换
        # 如果切换当前节点，则需要上一个节点
        # 如果切换下一个节点，这设置当前节点 对于 current_flow_node_done 的值
        # 当前批次的工作流，还没有涉及到节点切换
        if not self.values.get():
            self.printer_show("您还没有开始当前流程哦~",flow_chat_messages)
        else:
            CHAT_FLOW_STATE.set_state("current_flow_node_done", self.flow_node_name)

