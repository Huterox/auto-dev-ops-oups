"""
@FileName：system_state.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/3 15:58
@Copyright：©2018-2024 awesome!
"""

import streamlit as st


class CHAT_FLOW_STATE(object):


    @staticmethod
    def set_state(key, value):
        if not st.session_state.get("chat_flow_state"):
            st.session_state.chat_flow_state = {}
        st.session_state.chat_flow_state[key] = value

    @staticmethod
    def get_state(key):
        if not st.session_state.get("chat_flow_state"):
            st.session_state.chat_flow_state = {}
        return st.session_state.chat_flow_state.get(key,None)

    @staticmethod
    def delete_state(key):
        if not st.session_state.get("chat_flow_state"):
            st.session_state.chat_flow_state = {}
        del st.session_state.chat_flow_state[key]

    @staticmethod
    def clear_state():
        st.session_state.chat_flow_state = {}