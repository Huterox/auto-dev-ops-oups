"""
@FileName：step01.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/5 21:29
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.agents.agent import FlowAgent
from workflow.build_system.variables import FlowManger

"""
AgentStep3 是一个自动执行的节点机器人，
当前节点根据上面节点确定的输入，自动生成SQL语句，这里主要是创建表的SQL语句
"""
class AgentStep3(FlowAgent):

    """
    这个执行流程与step02的流程一致
    """
    def __builder_system_prompt(self,history,input_prompt):
        date_design_content = FlowManger.get_value("step02")
        current_sql = FlowManger.get_value("step03")
        if not current_sql:
            system_prompt = f"You are a SQL generator.You need to generate SQL " +\
                            f"statements based on the following input.The input is: {date_design_content}." +\
                            f"输出结果格式如下，注意只需要返回下述格式即可：" +\
                            """
                            **表名A：**
                            ```sql
                            创建SqlA
                            ```
                            **表名B：**
                            ```sql
                            创建SqlB
                            ```
                            """
        else:
            system_prompt = f"You are a SQL generator.You need to generate SQL " +\
                            f"这是你当前已经生成的SQL创建语句{current_sql}你需要根据用户提出的需求来修改，新增这些创建语句" +\
                            f"注意每次返回都需要返回全表的SQL语句，哪怕根据用户的需求，你只是修改了其中几个表，你也需要返回全部"+\
                            f"输出结果格式如下，注意只需要返回下述格式即可：" +\
                            """
                            **表名A：**
                            ```sql
                            创建SqlA
                            ```
                            **表名B：**
                            ```sql
                            创建SqlB
                            ```
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
        sys_prompt = self.__builder_system_prompt(history,input_prompt)
        # 注意当前的这个bot是没有完整的上下文记忆的，在这里使用的是singleChat，因此需要手动将结果给到
        # history当中去，但是这个给到history只是为了方便做展示记录，实际上不会参与到LLM推理当中去
        history = self.__build_input(history,input_prompt)
        res = self.singleChat(sys_prompt,input_prompt)
        # res = "ok"
        history.append({"role": "assistant", "content": res})
        return res

