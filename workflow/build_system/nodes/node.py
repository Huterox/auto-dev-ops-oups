"""
@FileName：node.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/5 21:27
@Copyright：©2018-2024 awesome!
"""
import time

import streamlit as st
class FlowNode(object):

    def get_index(self):
        pass

    def message_show(self, flow_chat_messages):
        pass

    def get_res(self, input_prompt: str, st, flow_chat_messages):
        pass


    def printer_show(self,msg):
        placeholder = st.empty()
        full_response = ''
        for item in msg:
            full_response += item
            time.sleep(0.02)
            placeholder.markdown(full_response)
        placeholder.markdown(full_response)

    # not all the flow node need have this function
    # if current node is the first node, it will have the previous node
    # else if current node is the last node, it will not have the previous node
    def next_flow_node(self,):
        pass

    # not all the flow node need to have this function
    def last_flow_node(self):
        pass

    def init_auto_func(self,*args):
        pass

    def variable_show(self):
        pass

    def described_show(self):
        pass



