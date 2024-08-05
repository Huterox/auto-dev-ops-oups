"""
@FileName：agents.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/4 14:14
@Copyright：©2018-2024 awesome!

Agents主要为实现整个逻辑推理的智能体，负责实现工作流程设定的复杂实现
"""
from bot.Bot import ChatBot


class FlowAgent(ChatBot):

    def __builder_system_prompt(self,history,input_prompt):
        pass

    def __build_input(self, history,input_prompt):
        pass

    def get_res(self, history: list,input_prompt:str):
        """
        :param history: [
            {"role": "assistant", "content": msg},
            {"role": "user", "content": msg}
        ]
        :param input: msg
        :return:
        """
        pass

class AgentStep1(FlowAgent):

    def __builder_system_prompt(self,history,input_prompt):
        return """你是一个基于下面内容的AI小助手，你的名字叫做小A"""

    def __build_input(self, history,input_prompt)->list:
        history.append({"role": "user","content":input_prompt})
        return history


    def get_res(self, history: list,input_prompt:str):
        """
        :param history: [
            {"role": "assistant", "content": msg},
            {"role": "user", "content": msg}
        ]
        :param input: msg
        :return:
        """
        sys_prompt = self.__builder_system_prompt(history,input_prompt)
        history = self.__build_input(history,input_prompt)
        res = self.muiltChat(history,sys_prompt)
        return res