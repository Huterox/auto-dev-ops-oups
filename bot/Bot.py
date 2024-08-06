"""
@FileName：Bot.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/20 17:15
@Copyright：©2018-2024 awesome!
"""
import os

import toml
from openai import OpenAI
from base import current_dir_root
"""
这里加载默认配置
"""
config = toml.load(os.path.join(current_dir_root, "api.toml"))
default_key = config["DEFAULT"]["default_key"]
default_base = config["DEFAULT"]["default_base"]
default_model = config["DEFAULT"]["default_model"]
default_temperature = config["DEFAULT"]["default_temperature"]
client = OpenAI(api_key=default_key,
                base_url=default_base,
                )

class ChatBot(object):

    def __init__(self):
        pass

    """
    进行单次对话，只进行一轮对话，没有上下文信息
    """
    def singleChat(self,system_prompt,question,temperature=default_temperature)->str:

            history_openai_format = []
            # 先加入系统信息
            history_openai_format.append(
                {"role": "system",
                 "content": system_prompt
                 },
            )
            history_openai_format.append(
                {"role": "user",
                 "content": question
                 },
            )
            completion = client.chat.completions.create(
                model=default_model,
                messages=history_openai_format,
                temperature=temperature,
            )
            try:
                result = completion.choices[0].message.content
            except Exception as e:
                print(e)
                result = "抱歉，出现异常，请稍后再试~"
            return result

    """
    多轮对话（保留历史信息）
    """
    def muiltChat(self,history:list[dict],system_prompt:str,temperature:float=default_temperature)->str:
        if(history==None):
            history = []
        history_format = history[:]
        # 在原来的记录的基础上，增加系统的提示词
        history_format.append({"role": "system", "content": system_prompt})
        completion = client.chat.completions.create(
                model=default_model,
                messages=history_format,
                temperature=temperature,
            )
        try:
            result = completion.choices[0].message.content
        except Exception as e:
            print(e)
            result = "抱歉，出现异常，请稍后再试~"
        # 将返回信息给到history当中去
        history.append({
            "role": "assistant",
            "content": result
        })
        return result

