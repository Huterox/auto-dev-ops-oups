"""
@FileName：agent.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/4 14:14
@Copyright：©2018-2024 awesome!

Agent主要为实现整个逻辑推理的智能体，负责实现工作流程设定的复杂实现
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
