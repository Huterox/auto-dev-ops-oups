"""
@FileName：flows.py
@Author：Huterox
@Description：Go For It
@Time：2024/8/4 14:17
@Copyright：©2018-2024 awesome!
"""
from workflow.build_system.nodes.node import FlowNode
from workflow.build_system.nodes.step01 import FlowNodeStep1
from workflow.build_system.nodes.step02 import FlowNodeStep2
from workflow.build_system.system_state import CHAT_FLOW_STATE

"""
工作流节点，负责管理整个工作流的节点
对Agent进行封装，除了需要实现具体的prompt和tools的调用之外（RAG本质上也就是Tools的调用）
还需要做如下事情：
1. 提供分支切换函数，同时完成分支切换
2. 按照要求流程将变量值设置在变量当中，便于其Agent调用

TODO: 现在暂时没有可视化创作界面，因此没有办法通过JSON模板去生成这样的FlowNode只能先进行编码
"""

"""
当前节点规划路线如下：
1. step01 负责对用户的需求进行整理 -- 手动触发下一步 有上下文
2. step02 负责根据用户的需求，来设计数据库，明确数据库的表名，字段名 -- 手动触发下一步 有上下文
3. step03 负责根据数据库的表设计，来生成数据库创建语句 -- 自动 无上下文
4. step04 根据数据库表设计，来生成系统的基本代码 -- 自动 无上下文
5. step05 根据当前的系统基本代码，来确定修改系统 -- 手动 但无上下文
"""

flow_step01 = FlowNodeStep1("step01")
flow_step02 = FlowNodeStep2("step02")
flow_step03 = FlowNodeStep2("step03")
flow_step04 = FlowNodeStep2("step04")
flow_step05 = FlowNodeStep2("step05")

flow_map = {
    "0":{
        "last":None,
        "next":"step01",
        "node":None
    },
    "step01":{
        "last":None,
        "next":"step02",
        "node":flow_step01
    },
    "step02": {
        "last": "step01",
        "next": "step03",
        "node": flow_step02
    },
    "step03": {
        "last": "step02",
        "next": "step04",
        "node": flow_step03
    },
    "step04": {
        "last": "step03",
        "next": "step05",
        "node": flow_step04
    },
    "step05": {
        "last": "step04",
        "next": None,
        "node": None
    }
}



class FlowNodeManger(object):
    # 这个FlowNodeManger的实现机制本质上其实就是通过system_state来进行处理的
    @staticmethod
    def getFlowNode()->FlowNode:
        # 如果当前状态里面没有FlowNode那么我们默认就将Step1给拿到作为当前的工作流
        flow_node = CHAT_FLOW_STATE.get_state("current_flow_node")
        if flow_node is None:
            flow_node = flow_map.get("step01").get("node")
            CHAT_FLOW_STATE.set_state("current_flow_node",flow_node)
        else:
            # 如果当前有节点，但是当前的节点已经执行完毕了，那么我们就要切换到下一个节点
            done_node_name = CHAT_FLOW_STATE.get_state("current_flow_node_done")

            if done_node_name:
                next_node_name = flow_map.get(done_node_name).get("next")
                flow_node = flow_map.get(next_node_name).get("node")
                CHAT_FLOW_STATE.set_state("current_flow_node", flow_node)

        return flow_node