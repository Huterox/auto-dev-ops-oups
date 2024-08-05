"""
@FileName：graph.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/27 21:17
@Copyright：©2018-2024 awesome!
"""

"""
在streamlit当中可视化工作流
"""
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
def graph_show_with_st():

    #image, circularImage, diamond, dot, star, triangle, triangleDown, hexagon, square and icon
    graph = {
        0:{
            "name":"开始",
            "size":20,
            "color":"Cyan",
            "shape":"star",
            "edges":[1]
        },
        1:{
            "name":"提出需求",
            "size":20,
            "color":"DeepSkyBlue",
            "shape":"circular",
            "edges":[2]
        },
        2:{
            "name":"对话与需求分析",
            "size":20,
            "color":"MediumSpringGreen",
            "shape":"circular",
            "edges": [1,3]
        },
        3:{
            "name":"确认需求",
            "size":20,
            "color":"LawnGreen",
            "shape":"circular",
            "edges": [4,1]
        },
        4:{
            "name":"数据建模",
            "size":20,
            "color":"DarkTurquoise",
            "shape":"circular",
            "edges": [5]
        },
        5:{
            "name":"对话与数据建模",
            "size":20,
            "color":"DarkCyan",
            "shape":"circular",
            "edges": [4,6]
        },
        6:{
            "name":"确认建模",
            "size":20,
            "color":"DarkTurquoise",
            "shape":"circular",
            "edges": [4,7]
        },
        7:{
            "name":"生成执行SQL执行脚本",
            "size":20,
            "color":"LightYellow",
            "shape":"circular",
            "edges": [8]
        },
        8:{
            "name":"代码生成插件工作",
            "size":20,
            "color":"Gold",
            "shape":"circular",
            "edges": [9]
        },
        9:{
            "name":"系统构建打包",
            "size":20,
            "color":"DarkOrange",
            "shape":"circular",
            "edges": [10]
        },
        10: {
            "name": "结束",
            "size": 20,
            "color": "OrangeRed",
            "shape": "star",
            "edges": []
        },
    }

    flow_nodes = []
    flow_edges = []
    for id,node in graph.items():
        t = Node(id=id,
             label=node.get("name"),
             size=node.get("size"),
             shape=node.get("shape"),
             color=node.get("color")
             )
        flow_nodes.append(t)
        for edge in node.get("edges"):
            e = Edge(source=id,
                 label=f"step{id}",
                 size=15,
                 target=edge,
                 )
            flow_edges.append(e)

    # 定义展示图
    flow_config = Config(width=1200,
                            height=360,
                            directed=True,
                            physics=True,
                            hierarchical=False,

                            # **kwargs
                )

    flow_config_return_value = agraph(nodes=flow_nodes,
                                             edges=flow_edges,
                                             config=flow_config,

                                      )