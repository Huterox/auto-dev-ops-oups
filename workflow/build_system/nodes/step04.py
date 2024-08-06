"""
@FileName：step01.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/5 21:26
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.agents.step04 import AgentStep4
from workflow.build_system.nodes.node import FlowNode
from workflow.build_system.variables import FlowVariables
from workflow.build_system.system_state import CHAT_FLOW_STATE
import streamlit_antd_components as sac
import streamlit as st
import time

class FlowNodeStep4(FlowNode):

    def __init__(self, name):
        self.agent = AgentStep4()
        self.flow_node_name = name
        self.index = 3
        self.values = FlowVariables("step04")
        self.values.set(
            {
                "dao": None,
                "controller": None,
                "view": None,
                "requirement_front": None,
                "requirement_back": None,
            }
        )
        # 这里单独再来一个变量
        self.value_code = FlowVariables("step04_code")

    def described_show(self):
        info = """
        当前节点为第四个节点主要负责生成基础系统代码🏎
        """
        sac.alert(label='节点描述',
                  description=info,
                  size=12,
                  banner=[False, True],
                  color='indigo',
                  icon=False,
                  variant='transparent',
                  closable=True)

    @st.experimental_dialog('变量',width="large")
    def variable_show(self):


        content = self.values.get()
        code_markdown = f"""
[TOC]
# 基础系统
## 基础系统Dao层代码
{content.get("dao")}
## 基础系统Controller层代码
{content.get("controller")}
## 基础系统前端代码 
{content.get("view")}
# 需求实现
## 需求后端代码
{content.get("requirement_back")}
## 需求前端代码
{content.get("requirement_front")}
        """
        st.download_button("下载项目代码",data=code_markdown,file_name="项目代码.md",mime="text/markdown")
        variable_show_step_4 = st.container(height=400)
        variable_show_step_4.write(code_markdown)
        # 这个变量在第最后一个微调的时候还用得上
        self.value_code.set(code_markdown)

    def get_index(self):
        return self.index

    def current_printer(self,msg):
        placeholder = st.empty()
        full_response = ''
        for item in msg:
            full_response += item
            time.sleep(0.002)
            placeholder.markdown(full_response)
        placeholder.markdown(full_response)

    def init_auto_func(self,flow_chat_messages):

        # 如果说当前没有设置的变量，那么就说明我们当前这个执行节点还是处于初始化的状态
        time.sleep(1)
        v = self.values.get()
        if v.get("dao")==None:
            with flow_chat_messages.chat_message("assistant"):
                self.printer_show("正在根据当前SQL创建语句生成基本系统Dao层代码....1️⃣")
                input_prompt = "请根据获取到的SQL创建语句，生成对应的Dao层代码，按照格式要求返回"
                with st.spinner("Dao层代码生成中"):
                    dao = self.agent.get_res("dao", input_prompt)
                    v["dao"] = dao
                    self.values.set(v)
                    # 将这些结果先临时存储起来（在展示的历史记录当中）
                    histroy = CHAT_FLOW_STATE.get_state("messages_step_4")
                    histroy.append({"role": "assistant", "content": dao})
                    CHAT_FLOW_STATE.set_state("messages_step_4", histroy)
                    self.current_printer(dao)

            with flow_chat_messages.chat_message("assistant"):
                self.printer_show("正在创建对应的系统基础接口代码，代码基于Fast API编写2️⃣")
                input_prompt = "请根据获取到的代码信息，生成对应的Controller层代码，按照格式要求返回"
                with st.spinner("Controller层代码生成中"):
                    controller = self.agent.get_res("controller", input_prompt)
                    v["controller"] = controller
                    self.values.set(v)
                    # 将这些结果先临时存储起来（在展示的历史记录当中）
                    histroy = CHAT_FLOW_STATE.get_state("messages_step_4")
                    histroy.append({"role": "assistant", "content": controller})
                    CHAT_FLOW_STATE.set_state("messages_step_4", histroy)
                    self.current_printer(controller)

            with flow_chat_messages.chat_message("assistant"):
                self.printer_show("正在创建对应的系统基础页面代码，代码基于Vue3与TypeScript编写3️⃣")
                input_prompt = "请根据获取到的代码信息，生成对应的前端代码，按照格式要求返回"
                with st.spinner("前端代码生成中"):
                    view = self.agent.get_res("view", input_prompt)
                    v["view"] = controller
                    self.values.set(v)
                    # 将这些结果先临时存储起来（在展示的历史记录当中）
                    histroy = CHAT_FLOW_STATE.get_state("messages_step_4")
                    histroy.append({"role": "assistant", "content": view})
                    CHAT_FLOW_STATE.set_state("messages_step_4", histroy)
                    self.current_printer(view)

            with flow_chat_messages.chat_message("assistant"):
                self.printer_show("正在创建对应的业务的后端代码，代码基于Fast API编写4️⃣")
                input_prompt = "请根据获取到的代码信息，生成对应的需求后端代码，按照格式要求返回"
                with st.spinner("需求后端代码生成中"):
                    requirement_back = self.agent.get_res("requirement_back", input_prompt)
                    v["requirement_back"] = controller
                    self.values.set(v)
                    # 将这些结果先临时存储起来（在展示的历史记录当中）
                    histroy = CHAT_FLOW_STATE.get_state("messages_step_4")
                    histroy.append({"role": "assistant", "content": requirement_back})
                    CHAT_FLOW_STATE.set_state("messages_step_4", histroy)
                    self.current_printer(requirement_back)

            with flow_chat_messages.chat_message("assistant"):
                self.printer_show("正在创建对应的业务的前端代码，代码基于Vue3与TypeScript编写5️⃣")
                input_prompt = "请根据获取到的代码信息，生成对应的需求前端代码，按照格式要求返回"
                with st.spinner("需求前端代码生成中"):
                    requirement_front = self.agent.get_res("requirement_back", input_prompt)
                    v["requirement_front"] = controller
                    self.values.set(v)
                    # 将这些结果先临时存储起来（在展示的历史记录当中）
                    histroy = CHAT_FLOW_STATE.get_state("messages_step_4")
                    histroy.append({"role": "assistant", "content": requirement_front})
                    CHAT_FLOW_STATE.set_state("messages_step_4", histroy)
                    self.current_printer(requirement_front)
                    self.printer_show("当前系统生成完毕，请查看Variable，获取项目markdown代码文件")



    def message_show(self, flow_chat_messages):
        if not CHAT_FLOW_STATE.get_state("messages_step_4"):
            CHAT_FLOW_STATE.set_state("messages_step_4",
                                      [
                                          {"role": "assistant", "content": "你好我是当前工作流的对话助手小D💨主要负责生成基础系统代码"}
                                      ]
                                      )
            # 项目助手对话的记录
        for msg in CHAT_FLOW_STATE.get_state("messages_step_4"):
            flow_chat_messages.chat_message(msg["role"]).write(msg["content"])

        # 这个节点的函数是默认自动处理的
        self.init_auto_func(flow_chat_messages)

        with flow_chat_messages:
            r_001, r_002 = st.columns([0.6, 0.4])
            with r_001:
                st.markdown("💥")
            with r_002:
                st.button("next04", on_click=self.next_flow_node, args=(flow_chat_messages,))

    def get_res(self, input_prompt: str, st, flow_chat_messages):
        # 这里注意我们当前的这个节点是没有对话的
        pass

    def next_flow_node(self,flow_chat_messages):
        # 记录一下，当前的节点执行完毕
        # 如果需要切换上一个节点，那么你要找到上一个节点的上一个节点才能完成切换
        # 如果切换当前节点，则需要上一个节点
        # 如果切换下一个节点，这设置当前节点 对于 current_flow_node_done 的值
        # 当前批次的工作流，还没有涉及到节点切换
        # 这个节点比较特殊
        if not self.values.get().get("dao"):
            self.printer_show("您还没有开始当前流程哦~",flow_chat_messages)
        else:
            CHAT_FLOW_STATE.set_state("current_flow_node_done", self.flow_node_name)
