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
import concurrent.futures
from base import current_dir_root
from bot.collection.agents import CollectionExtAgent
from webui.handler.collationHandler import getCollectionSummary, getCollectionSuggest, get_audio_content


@st.experimental_dialog('音频解析',)
def audio_analysis(st,container_show):
    audio_analysis_container = st.container(height=300)
    with audio_analysis_container:
        audio_path = st.session_state.get("collation_audio_input")
        # 先过一下提示
        if audio_path:
            if os.path.exists(audio_path):
                sac.alert(label='Tips',
                          description='音频已加载',
                          size=12,
                          color='teal',
                          banner=False,
                          icon=True, closable=True)
            else:
                sac.alert(label='Tips',
                          description='音频地址错误',
                          size=12,
                          color='yellow',
                          banner=False,
                          icon=True, closable=True)
                return
            # 之后在去解析音频
            # 展示解析结果
            sac.divider(label='`解析结果`', icon="lightning-charge", align='center', color='gray', key="5")
            audio_res_analysis_container = st.container(height=130)
            with audio_res_analysis_container:
                with st.spinner('正在解析语音...'):
                    with audio_res_analysis_container:
                        res,flag = get_audio_content(audio_path)
                        # 将当前提取的对话内容存储起来
                        st.session_state.current_audio_content = res
                        placeholder = st.empty()
                        full_response = ''
                        for item in res:
                            full_response += item
                            time.sleep(0.005)
                            placeholder.markdown(full_response)
                        placeholder.markdown(full_response)
                    if flag:
                        with st.spinner("正在整理需求..."):
                            agent = CollectionExtAgent()
                            ext = agent.get_ext(res)
                            # 临时存储ext，并展示
                            st.session_state["current_audio_content_ext"] = ext
                            container_show.empty()
                            with container_show.chat_message("assistant"):
                                placeholder = st.empty()
                                full_response = ''
                                for item in ext:
                                    full_response += item
                                    time.sleep(0.005)
                                    placeholder.markdown(full_response)
                                placeholder.markdown(full_response)
                            sac.alert(label='Tips',
                                      description='需求整理提取完毕',
                                      size=12,
                                      color='teal',
                                      banner=False,
                                      icon=True, closable=True)


        else:
            sac.alert(label='Tips',
                      description='请填写音频地址',
                      size=12,
                      color='yellow',
                      banner=False,
                      icon=True, closable=True)


def collationUI():
    config = toml.load(os.path.join(current_dir_root, "api.toml"))
    t0,t1 = st.columns([1,3])
    with t0:
        st.subheader("MathAI V0.1")
        st.caption("POWERED BY @Huterox")
    with t1:
        sac.alert(label='Tips',
                  description=f'如果对生成结果有较高要求，'
                              f'`侧边栏可折叠，此处页面将展示更多内容`。'
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

        # 先清空一下
        collation_summary_container.empty()
        if "collation_main_messages" not in st.session_state or st.session_state.collation_main_messages == []:
            with collation_summary_container.chat_message("assistant"):
                msg = "当前您还没有提出需求喔~，请您提出您的需求，我将为您总结需求😄"
                placeholder = st.empty()
                full_response = ''
                for item in msg:
                    full_response += item
                    time.sleep(0.005)
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        else:
            summary_content = st.session_state.get("collation_summary_content","暂无总结~")
            collation_summary_container.chat_message("assistant").write(summary_content)

        #######################################################################################
        st.session_state["collation_suggest_open"] = sac.switch(
            label='智能提示', align='center', size='md',
            value=st.session_state.get("collation_suggest_open", False),
        )

        collation_suggest_container = st.container(height=200)
        # 先清空一下
        collation_suggest_container.empty()
        if "collation_main_messages" not in st.session_state or st.session_state.collation_main_messages == []:
            with collation_suggest_container.chat_message("assistant"):
                msg = "当前您还没有提出需求喔~，请您提出您的需求，我将为您提出建议😄"
                placeholder = st.empty()
                full_response = ''
                for item in msg:
                    full_response += item
                    time.sleep(0.005)
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        else:
            suggest_content = st.session_state.get("collation_suggest_content","暂无建议👀")
            collation_suggest_container.chat_message("assistant").write(suggest_content)

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

            try:
                response = client.chat.completions.create(
                    model=default_model,
                    temperature=default_temperature,
                    messages=[
                        {"role": "system",
                         "content": "你是一个专业的软件开发项目经理，接下来你将基于用户的需求来与用户进行对接\n"},
                        {"role": "user", "content": prompt}
                    ])
                msg = response.choices[0].message.content
                st.session_state.collation_main_messages.append({"role": "assistant", "content": msg})
                """
                在这里完成请求之后，我们拿到history，去询问对应的agent
                """
                history = st.session_state.collation_main_messages
                # 并发请求 获取建议和总结
                # 2. 创建任务,并提交
                with concurrent.futures.ThreadPoolExecutor(
                        max_workers=2) as executor:  # 限制最大线程数

                    # 提交需求总结任务，用户需求提问建议任务
                    futures = [
                        executor.submit(getCollectionSummary, st,collation_summary_container,history),
                        executor.submit(getCollectionSuggest,st,collation_suggest_container,history)
                    ]
                    # 等待所有任务完成，等待所有信息展示
                    for future in concurrent.futures.as_completed(futures):
                        info = future.result()
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
        if not st.session_state.get("current_audio_content_ext"):
            collation_audio_container.empty()
            with collation_audio_container.chat_message("assistant"):
                msg = "请您输入音频文件地址，我将根据音频为您总结用户需求🥴"
                placeholder = st.empty()
                full_response = ''
                for item in msg:
                    full_response += item
                    time.sleep(0.01)
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        else:
            collation_audio_container.chat_message("assistant")\
                .write(st.session_state.get("current_audio_content_ext"))
        audio_path = st.session_state.get("collation_audio_input")
        if audio_path:
            if os.path.exists(audio_path):
                st.audio(data=audio_path)
            else:
                st.markdown("`音频地址错误`")
        else:
            st.markdown("`暂未填写音频文件地址`")
        audio_input_path = st.text_input("请输入音频文件地址")
        st.session_state["collation_audio_input"] = audio_input_path
        if st.button("开始提取音频内容",type="primary"):
            audio_analysis(st,collation_audio_container)

