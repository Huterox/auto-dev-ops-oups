"""
@FileName：step01.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/5 21:29
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.agents.agent import FlowAgent


class AgentStep1(FlowAgent):

    def __builder_system_prompt(self,history,input_prompt):
        return """你是一个软件项目经理小A，你负责根据用户的需求，来设计软件的功能，功能描述要求详细，使用中文来回答问题"""

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
