"""
@FileName：RequirementsCollation.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/20 15:41
@Copyright：©2018-2024 awesome!
"""

import os
import toml
import time
import streamlit as st
import streamlit_antd_components as sac
from openai import OpenAI

from base import current_dir_root

def collationUI():
  config = toml.load(os.path.join(current_dir_root, "api.toml"))
  t0,t1 = st.columns([1,3])
  with t0:
    st.subheader("MathAI V0.1")
    st.caption("POWERED BY @Huterox")
  with t1:
    sac.alert(label='Tips',
              description=f'如果对生成结果有较高要求，'
                          f'建议在【首页】设置处，设置高性能模型🌎'
                          f'\n点击生成逻辑图，可以根据当前需求生成逻辑图'
                          f'\n音频提取当前基于Whisper实现（当前内置集成tiny模型）'
                          ,
              color='success',
              banner=False,
              icon=True, closable=True)

  c0,c1,c2 = st.columns([1,2,1])
  with c0:
    # 这里是两个提示总结框
    st.session_state["collation_summary_open"]=sac.switch(
        label='智能总结', align='center', size='md',
        value=st.session_state.get("collation_summary_open", False),
      )
    collation_summary_container = st.container(height=200)
    st.button("生成逻辑图",type="primary")
    with collation_summary_container.chat_message("assistant"):
      msg = "当前您还没有提出需求喔~，请您提出您的需求，我将为您总结需求😄"
      placeholder = st.empty()
      full_response = ''
      for item in msg:
        full_response += item
        time.sleep(0.01)
        placeholder.markdown(full_response)
      placeholder.markdown(full_response)

    st.session_state["collation_suggest_open"] = sac.switch(
        label='智能提示', align='center', size='md',
        value=st.session_state.get("collation_suggest_open", False),
      )
    collation_suggest_container = st.container(height=200)
    with collation_suggest_container.chat_message("assistant"):
      msg = "当前您还没有提出需求喔~，请您提出您的需求，我将为您提出建议😄"
      placeholder = st.empty()
      full_response = ''
      for item in msg:
        full_response += item
        time.sleep(0.01)
        placeholder.markdown(full_response)
      placeholder.markdown(full_response)

  with c1:
    # 这个是主对话框
    collation_main_container = st.container(height=500)
    if "collation_main_messages" not in st.session_state or st.session_state.collation_main_messages==[]:
      st.session_state["collation_main_messages"] = []
      collation_main_container.chat_message("assistant").write("我是一个专业的需求分析小助理，您将作为用户与我进行需求对接👀")
    # 加载历史消息
    for msg in st.session_state.collation_main_messages:
        collation_main_container.chat_message(msg["role"]).write(msg["content"])
    # 加载大模型相关配置
    default_key = config["DEFAULT"]["default_key"]
    default_base = config["DEFAULT"]["default_base"]
    default_model = config["DEFAULT"]["default_model"]
    default_temperature = config["DEFAULT"]["default_temperature"]
    if (default_base != None and default_model != ""):
      placeholder = "有什么我可以帮你的么？😀"
    else:
      placeholder = "有什么我可以帮你的么？😀(请先设置默认大模型KEY)"
    if prompt := st.chat_input(placeholder=placeholder):
      client = OpenAI(api_key=default_key,
                      base_url=default_base,
                      )
      # 添加对话历史信息
      st.session_state.collation_main_messages.append({"role": "user", "content": prompt})
      collation_main_container.chat_message("user").write(prompt)
      response = client.chat.completions.create(
        model=default_model,
        temperature=default_temperature,
        messages=[
          {"role": "system",
           "content": "你是一个专业的软件开发项目经理，接下来你将基于用户的需求来与用户进行对接\n"},
          {"role": "user", "content": prompt}
        ])
      try:
        msg = response.choices[0].message.content
        st.session_state.collation_main_messages.append({"role": "assistant", "content": msg})
      except Exception as e:
        msg = "抱歉，出现异常，请稍后再试~"
      with collation_main_container.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ''
        for item in msg:
          full_response += item
          time.sleep(0.01)
          placeholder.markdown(full_response)
        placeholder.markdown(full_response)

  with c2:
    # 侧边音频提取总结 f'当前仅支持普通话&英文'
    sac.alert(label='Tips',
              description=f'当前仅支持普通话&英文',
              size=13,
              color='success',
              banner=False,
              icon=True, closable=True)
    collation_audio_container = st.container(height=250)
    with collation_audio_container.chat_message("assistant"):
      msg = "请您输入音频文件地址，我将根据音频为您总结用户需求🥴"
      placeholder = st.empty()
      full_response = ''
      for item in msg:
        full_response += item
        time.sleep(0.01)
        placeholder.markdown(full_response)
      placeholder.markdown(full_response)
    st.audio(data=None)
    st.text_input("请输入音频文件地址", key="collation_audio_input")