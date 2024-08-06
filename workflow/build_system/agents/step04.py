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
系统生成部分，将由多个子任务模块构成，分别是：
1. SQL --> Python代码 生成对应的DAO Controller Vue 代码
2. 需求 --> 基于刚刚生成的基础代码，去生成对应的业务代码
"""
"""
注意这里依然是链式调用，因为还是需要完整的上下文去生成
"""
class AgentStep4(FlowAgent):
    """
    在第4步当中，我们的变量的格式是这样的：
    {
        "dao":markdown,
        "controller":markdown,
        "view":markdown,
        "requirement_front":markdown,
        "requirement_back":markdown,
    }
    """

    def __get_dao_system_promot(self):
        sql_content = FlowManger.get_value("step03")
        system_prompt = f"""
        你是一个Python代码生成器，你需要通过SQL语句生成对应的DAO代码，要求：使用SQLAlchemy框架来实现，
        下面是SQL语句：
        {sql_content}
        代码格式如下，注意请按照如下格式回复：
        控制层代码文件结构如下：
        models
        ├── TableA.py
        ├── TableB.py
        session.py
        
        orm数据库连接代码: models/session.py 
         ```python
            代码内容
        ```
        表A 实体类代码: models/TableA.py
          ```python
            代码内容
        ```
        
        表B 实体类代码: models/TableB.py
          ```python
            代码内容
        ```
        表A 增删查改代码: dao/TableA.py
         ```python
            代码内容
        ```
        表B 增删查改代码: dao/TableB.py
        ```python
            代码内容
        ```
        """
        return system_prompt

    def __get_controller_system_promot(self):
        codes = FlowManger.get_value("step04")
        dao_code = codes.get("dao")
        system_prompt = f"""
        你是一个Python代码生成器,接下来你需要参考以下dao层的代码来生成controller层的代码:
        {dao_code}
        来生成对应的Controller代码，要求：使用FastApi框架来实现，通过路由分组将模块组合，代码格式如下，注意请按照如下格式回复：
        控制层代码文件结构如下：
        controller
        ├── TableA.py
        ├── TableB.py
        main.py
        
        主代码：main.py 
        ```python
            代码内容（各个模块的路由分组）
        ```
        
        表A curd代码: controller/TableA.py
         ```python
            代码内容
        ```
        
        表B curd代码: controller/TableB.py
           ```python
            代码内容
        ```
        """
        return system_prompt



    def __get_view_system_promot(self):

        codes = FlowManger.get_value("step04")
        dao_code = codes.get("dao")
        controller = codes.get("controller")
        system_prompt = f"""
        你是一个Vue代码生成器,接下来你需要通过以下dao代码和controller层的代码来生成前端视图层的代码
        css假设默认使用Tailwind CSS 组件默认使用 element-ui-plus 我们默认使用vue3进行编写:
        dao层代码如下：
        {dao_code}
        controller代码如下：
        {controller}
        注意请按照如下格式回复：
        前端代码文件结构如下：
        pages
        ├── pageTableA.vue
        ├── pageTableB.vue
        requests
        ├── requestTableA.ts
        ├── requestTableB.ts
   
        表A对应前端请求代码: requests/requestTableA.ts
        ```ts
            请求代码
        ```
        表A对应前端视图代码: pages/pageTableA.vue
         ```vue
            代码内容（调用对应请求代码）
        ```
        
        表B对应前端请求代码: requests/requestTableB.ts
        ```ts
            请求代码
        ```
        表B对应前端视图代码: pages/pageTableB.vue
         ```vue
            代码内容（调用对应请求代码）
        ```
        """
        return system_prompt

    def __get_requirement_front_system_promot(self):

        codes = FlowManger.get_value("step04")
        requirements_content = FlowManger.get_value("step01")
        dao_code = codes.get("dao")
        controller = codes.get("controller")
        system_prompt = f"""
          你是一个资深全栈程序员,你需要结合现在有的系统代码和用户的需求来编写后端的业务代码
          要求：使用FastApi框架来实现，通过路由分组将模块组合，
          当前已有的dao层代码是通过SQLAlchemy框架来实现的。
          现有的系统代码如下：
          {dao_code}
          {controller}
          用户需求如下：
          {requirements_content}
          代码格式如下，注意请按照如下格式回复：
          用户需求实现代码如下：
            requirements
            ├── controller
            ├──├──需求1（英文名称，根据需求进行适当命名）.py
            ├──├──需求2（英文名称，根据需求进行适当命名）.py
            ├── dao
            ├──├──需求1（英文名称，根据需求进行适当命名）.py
            ├──├──需求2（英文名称，根据需求进行适当命名）.py
            main.py
            
            主代码：main.py 
            ```python
                代码内容（各个模块的路由分组）
            ```
            requirements/controller/需求1（英文名称，根据需求进行适当命名）.py
             ```python
                代码内容
            ```
            requirements/dao/需求1（英文名称，根据需求进行适当命名）.py
             ```python
                代码内容
            ```
            
            requirements/controller/需求2（英文名称，根据需求进行适当命名）.py
            ```python
                代码内容
            ```
            requirements/dao/需求2（英文名称，根据需求进行适当命名）.py
             ```python
                代码内容
            ```
          """
        return system_prompt

    def __get_requirement_back_system_promot(self):
        codes = FlowManger.get_value("step04")
        requirements_back_content = codes.get("requirement_back")
        system_prompt = f"""
           你是一个资深全栈程序员,你需要结合现在有的系统代码和用户的需求来编写后端的业务代码
           css假设默认使用Tailwind CSS 组件默认使用 element-ui-plus 我们默认使用vue3进行编写:
           现在我们有一些后台代码，这些代码对应了实现的后台需求，需要做的是生成对应的前端代码
      
           用户需求如下：
           {requirements_back_content}
           代码格式如下，注意请按照如下格式回复：
           用户需求实现代码如下：
            pages
            ├──需求1（英文名称，根据需求进行适当命名）.vue
            ├──需求2（英文名称，根据需求进行适当命名）.vue
            requests
            ├──需求1（英文名称，根据需求进行适当命名）.ts
            ├──需求2（英文名称，根据需求进行适当命名）.ts
          
            需求1对应前端请求代码: requests/需求1（英文名称，根据需求进行适当命名）.ts
            ```ts
                请求代码
            ```
            需求1对应前端视图代码: pages/需求1（英文名称，根据需求进行适当命名）.vue
             ```vue
                代码内容（调用对应请求代码）
            ```
            
            需求2对应前端请求代码: requests/需求2（英文名称，根据需求进行适当命名）.ts
            ```ts
                请求代码
            ```
            需求1对应前端视图代码: pages/需求2（英文名称，根据需求进行适当命名）.vue
             ```vue
                代码内容（调用对应请求代码）
            ```
           """
        return system_prompt

    def __init__(self):
        super().__init__()
        self.system_prompt_map = {
            "requirement_back":self.__get_requirement_back_system_promot,
            "requirement_front":self.__get_requirement_front_system_promot,
            "dao":self.__get_dao_system_promot,
            "controller":self.__get_controller_system_promot,
            "view":self.__get_view_system_promot
        }

    def __builder_system_prompt(self,prompt_type):
        system_prompt = self.system_prompt_map.get(prompt_type)
        return system_prompt

    def __build_input(self, history,input_prompt)->list:
        history.append({"role": "user","content":input_prompt})
        return history


    def get_res(self, prompt_type: str,input_prompt:str):
        """
        :param history: [
            {"role": "assistant", "content": msg},
            {"role": "user", "content": msg}
        ]
        :param input: msg
        :return:
        """
        # 注意这里是单次对话，并且在这个模块里面啥都不管
        # sys_prompt = self.__builder_system_prompt(prompt_type)
        # res = self.singleChat(sys_prompt,input_prompt)
        # return res
        return "OK"
