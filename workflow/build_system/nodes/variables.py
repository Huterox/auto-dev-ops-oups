"""
@FileName：variables.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/4 14:18
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.system_state import CHAT_FLOW_STATE

"""
同样的道理，其本质上其实就是对状态的封装管理
"""
class FlowVariables(object):

    def __init__(self,name):
        self.name = name

    def set(self,value):
        CHAT_FLOW_STATE.set_state("FlowVariables"+self.name,value)

    def get(self):
        return CHAT_FLOW_STATE.get_state("FlowVariables"+self.name)

    def delete(self):
        CHAT_FLOW_STATE.delete_state("FlowVariables"+self.name)