"""
@FileName：homeHandler.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/20 17:36
@Copyright：©2018-2024 awesome!
"""
import os
import time

import toml
from openai import OpenAI
from base import current_dir_root
import streamlit_antd_components as sac


def home_assistant(st,doc,config):
    messages = st.container(height=470)
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "我是本项目的AI小助手，有什么可以帮你的么?"}]

    for msg in st.session_state.messages:
        messages.chat_message(msg["role"]).write(msg["content"])

    default_key = config["DEFAULT"]["default_key"]
    default_base = config["DEFAULT"]["default_base"]
    default_model = config["DEFAULT"]["default_model"]
    default_temperature = config["DEFAULT"]["default_temperature"]
    if(default_base!=None and default_model!=""):
        placeholder = "有什么我可以帮你的么？😀"
    else:
        placeholder = "有什么我可以帮你的么？😀(请先设置默认大模型KEY)"
    if prompt := st.chat_input(placeholder=placeholder):
        client = OpenAI(api_key=default_key,
                        base_url=default_base,
                        )
        st.session_state.messages.append({"role": "user", "content": prompt})
        messages.chat_message("user").write(prompt)
        try:
            response = client.chat.completions.create(
                model=default_model,
                temperature=default_temperature,
                messages=[
                    {"role": "system",
                     "content": "你是一个基于下面内容的AI小助手，请基于下面的内容和自己的知识回答用户问题。\n" + doc},
                    {"role": "user", "content": prompt}
                ])
            msg = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            msg = "抱歉，出现异常，请稍后再试~"
        with messages.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ''
            for item in msg:
                full_response += item
                time.sleep(0.01)
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
        # messages.chat_message("assistant").write_stream(msg)


def home_settings(st,config):
    load_config_in_state(st, config)
    st.write("##### 模型配置")
    st.write("")
    col1, col2 = st.columns([0.6, 0.4], gap="large")
    with col1:
        area = st.container(height=450)
        # 对相关的API进行设置（设置已经绑定了对应的st.session_state）
        # 这里默认使用的是 OpenAI 的模型（这里使用的是中转站）
        area.write('''##### ```官网：https://openai.com/```''')
        area.write('')
        new_openai_key = area.text_input("**API-KEY：**", st.session_state.default_key)
        area.write('')
        new_openai_base = area.text_input("**API-BASE：**", st.session_state.default_base)
        st.session_state.default_key = new_openai_key
        st.session_state.default_base = new_openai_base
        area.write('')
        new_temperature = area.slider("**Temperature：**", min_value=0.0, max_value=1.0, step=0.1,
                                      value=st.session_state.default_temperature)
        st.session_state.default_temperature = new_temperature

    with col2:
        area2 = st.container(height=450)
        with area2:
            default_mode =  config["DEFAULT"]["default_model"]
            model_list = ['gpt-4o-mini','gpt-4o','gpt-4-0125-preview',
                          'gpt-4-32k','gpt-4-0613','gpt-3.5-turbo','gpt-3.5-turbo-instruct'
                          ,'gpt-3.5-turbo-16k'
                          ]

            default_model = sac.segmented(
                items=[
                    sac.SegmentedItem(label=model_name) for model_name in model_list
                ], label='模型选择',
                align='center', direction="vertical", radius='lg',
                use_container_width=True,index=model_list.index(default_mode)
            )
            st.session_state.default_model = default_model
    st.write("")
    if st.button('保存', use_container_width=True, type="primary"):
        save_config_in_state(st, config)


def load_config_in_state(st, config):

    default_key = config["DEFAULT"]["default_key"]
    default_base = config["DEFAULT"]["default_base"]
    default_model = config["DEFAULT"]["default_model"]
    default_temperature = config["DEFAULT"]["default_temperature"]
    st.session_state.default_key = default_key
    st.session_state.default_base = default_base
    st.session_state.default_model = default_model
    st.session_state.default_temperature = default_temperature


def save_config_in_state(st,config):
    config["DEFAULT"]["default_key"] = st.session_state.default_key
    config["DEFAULT"]["default_base"] = st.session_state.default_base
    config["DEFAULT"]["default_model"] = st.session_state.default_model
    config["DEFAULT"]["default_temperature"] = st.session_state.default_temperature
    with open(os.path.join(current_dir_root, "api.toml"), 'w', encoding='utf-8') as file:
        toml.dump(config, file)
    st.toast("保存成功！", icon=":material/task_alt:")