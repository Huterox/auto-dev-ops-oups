"""
@FileName：variables.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/4 14:18
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.system_state import CHAT_FLOW_STATE

"""
The FlowVariables class is used to store variables within the flow.
It provides methods to set, get, and delete variables.
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

"""
The FlowVariableManger is a singleton class that manages the FlowVariables instances.
The FlowVariables is set in the st.session_state in current version! so we could get the FlowVariables values
by st.session_state. For better to manager the variable we design this manger!
"""

class FlowManger(object):

    @staticmethod
    def get_value(key):
        return CHAT_FLOW_STATE.get_state("FlowVariables"+key)

    @staticmethod
    def set_value(key,value):
        variable = FlowVariables(key)
        variable.set(value)