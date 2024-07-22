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
    def singleChat(self,system_prompt,question,temperature):

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
            result = completion.choices[0].message.content
            return result

    """
    多轮对话（保留历史信息）
    """
    def muiltChat(self,history:list[dict],message:str,temperature:float=0.5)->tuple[str,list[dict]]:
        if(history==None):
            history = []
        history.append({"role": "user","content":message})
        completion = client.chat.completions.create(
                model=default_model,
                messages=history,
                temperature=temperature,
            )
        result = completion.choices[0].message.content
        # 将返回信息给到history当中去
        history.append({
            "role": "user",
            "content": result
        })
        return result,history

