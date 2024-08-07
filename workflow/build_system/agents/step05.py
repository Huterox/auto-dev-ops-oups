"""
@FileName：step01.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/5 21:29
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.agents.agent import FlowAgent
from workflow.build_system.variables import FlowManger


class AgentStep5(FlowAgent):

    def __builder_system_prompt(self):
        code_markdown = FlowManger.get_value("step04_code")
        system_prompt = f"""
        你是一个资深程序员，接下来你需要参考用户的代码来协助用户编写，或者修改代码完成新的功能。
        下面是用户的代码{code_markdown},
        请你根据用户的需求来回答用户的问题，并给出代码，注意你需要说明清楚每一步的操作步骤。
        """
        return system_prompt

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
        history.append({"role": "user","content":input_prompt})
        sys_prompt = self.__builder_system_prompt()
        res = self.singleChat(sys_prompt,input_prompt)
        # res = "ok"
        history.append({"role": "assistant","content":res})
        return res