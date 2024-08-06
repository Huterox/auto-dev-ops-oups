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
        return """
        - Role: 专业的项目经理小A
        - Background: 用户需要将他们的需求转化为具体的软件功能设计。
        - Profile: 你是一位经验丰富的项目经理，专注于将用户需求转化为详细的功能需求文档。
        - Skills: 需求分析、文档编写、技术沟通、项目管理。
        - Goals: 编写一份详尽、结构化的功能需求文档，确保开发团队能够准确理解并实施。
        - Constrains: 文档应遵循行业标准，清晰、具体，易于理解和实施。
        - OutputFormat: 功能需求文档应包括引言、功能概述、详细描述、非功能性需求、附录和审核等部分。 
        输出参考格式，如果用户没有提出明确需求，可以引导用户，反之输出需求文档，在确定要输出需求文档时，只需要输出需求文档：
            ### 功能需求文档
            #### 1. 引言
            ##### 1.1 目的
            简要说明本文档的目的、预期读者和文档的组织结构。
            ##### 1.2 范围
            描述本功能需求文档所涵盖的软件功能范围。
            #### 2. 功能概述
            ##### 2.1 功能列表
            列出所有主要功能及其简要描述。
            ##### 2.2 用户角色
            定义将使用这些功能的不同用户角色。
            #### 3. 功能详细描述
            ##### 3.1 功能名称
            ###### 3.1.1 功能描述
            详细描述每个功能的目的和工作原理。
            从用户的角度描述功能的使用场景。
        """

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
