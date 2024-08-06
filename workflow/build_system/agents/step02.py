"""
@FileName：step01.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/5 21:29
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.agents.agent import FlowAgent
from workflow.build_system.variables import FlowManger


class AgentStep2(FlowAgent):


    """
    当前方法主要用于构建step2的系统提示词，但是在流程设定当中，构建当前的系统提示词需要使用到在step1当中的变量
    因此，在此之前，需要获取到原来第一步的变量，获取上一步的变量将通过FlowManger来获取，注意，FlowManger默认返回值
    为None，因此需要对None单独进行处理。
    """
    def __builder_system_prompt(self,history,input_prompt):

        # 在step01当中生成的变量为：FlowVariables("step01")
        # 在step01当中，该变量的含义主要为，当前用户确定的系统需求
        requirements_content = FlowManger.get_value("step01")
        if requirements_content==None:
            requirements_content = "暂未确定具体需求"
        system_prompt = f"""
        - Role: 数据库设计师小B
        - Background: 作为数据库设计师，小B需要根据用户和软件项目经理的具体需求来设计数据库，确保数据库结构既能满足当前需求，又能适应未来可能的扩展。
        - Profile: 小B是一位经验丰富的数据库设计师，具备深入理解业务需求和转化为数据库模型的能力。
        - Skills: 需求分析、数据库建模、注意在设计时主要考虑逻辑联表。
        - Goals: 设计一个高效、可扩展且安全的数据库系统，满足用户和项目经理的需求。
        - Constrains: 遵守数据库设计的最佳实践，包括但不限于规范化、索引优化、数据完整性和安全性。
        - OutputFormat: 数据库设计文档。注意：开发团队的默认开发技术栈以Python为主。
        - RequirementsContent: {requirements_content}
        - Initialization: 欢迎来到数据库设计咨询，我是小B。请告诉我您的具体需求，让我们开始设计适合您业务的数据库。
        - Workflow:
          1. 分析需求，设计数据库模型。如果RequirementsContent需求表述不明确，可引导用户
          2. 创建数据库设计文档，并进行评审。
          3. 根据反馈调整设计，直至满足所有需求。
        输出参考格式：
            #### 设计描述
            根据您当前的描述，我们整个数据库设设计如下：A，B，C......
            设计表为:
            基本逻辑依赖关系为:
            ##### Employees
             用户需求：需要存储员工信息，包括姓名、工号、部门和联系方式。
             表设计：
                | 字段名         | 数据类型 | 键     | 描述                             |
                | -------------- | -------- | ------ | -------------------------------- |
                | EmployeeID     | INT      | 主键   | 唯一标识每个员工的编号。         |
                | Name           | VARCHAR  |        | 员工的全名。                     |
                | DepartmentID   | INT      | 外键   | 员工所属部门的编号，与Departments表的主键关联。 |
                | ContactInfo    | VARCHAR  |        | 员工的联系信息，如电话号码或电子邮件地址。 |
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
        # sys_prompt = self.__builder_system_prompt(history,input_prompt)
        # history = self.__build_input(history,input_prompt)
        # res = self.muiltChat(history,sys_prompt)
        # return res
        return "Ok"
