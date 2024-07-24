"""
@FileName：agents.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/23 23:27
@Copyright：©2018-2024 awesome!
"""
from bot.Bot import ChatBot

"""
按照我们的要求去实例化两个agent，一个负责给出需求总结，一个负责给用户提问建议
注意：CollectionSummaryAgent，CollectionQuestionAgent 需要在bot回答完毕之后再进行触发
"""

class CollectionSummaryAgent(ChatBot):

    def __builder_system_prompt(self):
        sys_prompt = """
             您好，作为资深项目经理B，您将负责分析一段项目经理与用户之间的历史对话，并从中提取和总结项目需求。以下是您的任务指导和步骤：
             任务指导：
             - 仔细阅读历史对话，理解用户的需求和项目经理的回答。
             - 识别对话中的关键信息点，包括用户的期望、项目经理的澄清问题和解决方案。
             - 确保需求的总结基于对话内容，避免添加个人推断。

             任务步骤：
             1. 阅读并分析提供的历史对话，历史对话将给予倒叙内容
             2. 识别对话中用户明确表达的需求和期望。
             3. 注意项目经理是如何通过提问来澄清需求的。
             4. 使用中文，将需求点清晰、准确地总结成列表或段落形式。

             示例：
             假设历史对话中包含以下内容：

             用户：“我们需要一个能够处理大量数据的系统，并且数据需要实时更新。”
             项目经理A：“您能具体说明‘大量数据’是指多少吗？同时，实时更新的频率是多少？”
             用户：“我们每天大约有10TB的数据需要处理，更新频率至少需要达到每秒1次。”
             项目经理A：“明白了。我们会设计一个能够满足这些性能要求的系统。”

             需求总结：
             - 系统需要能够每天处理至少10TB的数据量。
             - 数据更新频率至少为每秒1次。

             请根据以上步骤和示例，从提供的历史对话中提取并总结项目需求。请注意，你只需要回答需求总结，不需要回答其他内容。
             """
        return sys_prompt


    def __build_input(self,history):
        input_prompt = """"""
        # 逆序
        input_prompt += "\n".join(
            [f"{'项目经理A' if item['role'] == 'assistant' else '用户'}:{item['content']}" for item in history[::-1]])
        return input_prompt


    def get_summary(self,history:list):
        """
        :param history: [
            {"role": "assistant", "content": msg}
            {"role": "user", "content": msg}
            ]
        :param input: msg
        :return:
        """
        # 构造系统提示词
        sys_prompt = self.__builder_system_prompt()
        input_prompt = self.__build_input(history)
        res = self.singleChat(sys_prompt,input_prompt)
        return res

class CollectionQuestionAgent(ChatBot):
    def __builder_system_prompt(self):
        sys_prompt = """
        您好，作为项目经理或团队成员，您将负责从历史对话中提出问题，以帮助澄清和深化项目需求。以下是您的任务指导和步骤：
        任务指导：
        - 仔细阅读历史对话，历史对话将给予倒叙内容，理解用户的需求和项目经理的回答。
        - 识别对话中的模糊点或需要进一步澄清的地方。
        - 构思具体、针对性的问题，以获取更多信息。
        - 使用开放式问题鼓励用户分享更多细节，同时注意问题的逻辑性和连贯性。
        
        任务步骤：
        1. 阅读并分析提供的历史对话。
        2. 识别对话中用户明确表达的需求和期望。
        3. 注意项目经理是如何通过提问来澄清需求的。
        4. 构思并提出有助于进一步明确需求的问题。
        
        示例：
        假设历史对话中包含以下内容：
        
        - 用户：“我们需要一个能够处理大量数据的系统，并且数据需要实时更新。”
        - 项目经理A：“您能具体说明‘大量数据’是指多少吗？同时，实时更新的频率是多少？”
        
        基于对话的提问示例：
        您提到需要支持多种文件格式，能否具体说明是哪些格式？例如，是否包括PDF、Word文档或Excel电子表格等？
        除了基本的打开和查看功能外，对于这些文件格式，是否还需要支持编辑或其他特定操作？
        
        请根据以上步骤和示例，根据历史对话内容提出有助于澄清和深化项目需求的问题。
        请注意，你只需要回答提问建议，不需要回答其他内容！
        """
        return sys_prompt

    def __build_input(self,history):
        input_prompt = """"""
        # 逆序
        input_prompt += "\n".join(
            [f"{'项目经理A' if item['role'] == 'assistant' else '用户'}:{item['content']}" for item in history[::-1]])
        return input_prompt

    def get_suggest(self,history:list):
        """
        :param history: [
            {"role": "assistant", "content": msg},
            {"role": "user", "content": msg}
        ]
        :param input: msg
        :return:
        """
        # 构造系统提示词
        sys_prompt = self.__builder_system_prompt()
        input_prompt = self.__build_input(history)
        res = self.singleChat(sys_prompt,input_prompt)
        return res