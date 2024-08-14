"""
@FileName：step01.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/5 21:26
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.agents.step03 import AgentStep3
from workflow.build_system.nodes.node import FlowNode
from workflow.build_system.variables import FlowVariables
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
        当前节点为第三个节点主要负责生成数据库SQL代码🎠
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
        variable_show_step_3 = st.container(height=500)
        variable_show_step_3.chat_message("assistant").write(self.values.get())

    def get_index(self):
        return self.index


    def init_auto_func(self,flow_chat_messages):

        # 如果说当前没有设置的变量，那么就说明我们当前这个执行节点还是处于初始化的状态
        v = self.values.get()
        if not v:
            time.sleep(1)
            input_prompt = "请根据你获取到的数据库建模文档，去生成对应的SQL创建语句，注意在创建语句当中需要加上注释。不要在数据库层面使用外键，但是可以在注释当中标注逻辑外键"
            with flow_chat_messages.chat_message("assistant"):
                self.printer_show("正在根据您的的文档分析，请稍等......")
            time.sleep(1)
            with flow_chat_messages.chat_message("assistant"):
                self.printer_show("正在结合建模文档，生成对应的SQL创建语句......")

            with flow_chat_messages.chat_message("assistant"):
                self.printer_show("接下来将进行SQL语句生成，请注意，点击右侧Variable可查看生成的SQL语句（当前对话框也可查看），"
                                  "查看后请点击Describe，避免默认打开结果查看弹窗0️⃣")

            with flow_chat_messages.chat_message("assistant"):
                with st.spinner("生成创建SQL语句当中......"):
                    histroy = CHAT_FLOW_STATE.get_state("messages_step_3")
                    msg = self.agent.get_res(histroy, input_prompt)
                    # 这里需要将变量写进去  （当前只是确定需求，还可以这样处理没有问题）
                    self.values.set(msg)
                    # 将记录写进去(是的，这里也是需要将变量写进去的，不然下次就会继续触发这个玩意)
                    # 当前的这个用户输出还是要去掉的
                    CHAT_FLOW_STATE.set_state("messages_step_3", histroy)
                    placeholder = st.empty()
                    full_response = ''
                    for item in msg:
                        full_response += item
                        time.sleep(0.002)
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)


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

        # 如果触发状态为这个，那么说明当前首次进入当前的节点，按照我们对流程的设计，在这里我们需要先进行初始化处理
        self.init_auto_func(flow_chat_messages)

        with flow_chat_messages:
            r_001, r_002 = st.columns([0.6, 0.4])
            with r_001:
                st.markdown("🛹")
            with r_002:
                st.button("next03", on_click=self.next_flow_node, args=(flow_chat_messages,))

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
