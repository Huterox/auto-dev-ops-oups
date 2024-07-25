"""
@FileName：SQLAssistant.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/22 16:23
@Copyright：©2018-2024 awesome!
"""
import os
import streamlit as st
import streamlit_antd_components as sac
import toml
from base import current_dir_root
from webui.handler.sqlHandler import SqlAssistantHelper, sql_chat_assistant
from streamlit_agraph import agraph, Node, Edge, Config

"""
sql助手（填写数据库地址，之后的话，开始对当前数据库的内容进行问答）
"""
def sqlAssistantUI():
    st.subheader("MathAI V0.1")
    st.caption("POWERED BY @Huterox")
    sql_assistant_select = sac.tabs([
        sac.TabsItem(label='SQL设置', icon='gear'),
        sac.TabsItem(label='SQL助手', icon='robot')
    ], align='center', variant='outline', use_container_width=True, index=0)

    # *******************助手和设置部分***************************
    config = toml.load(os.path.join(current_dir_root, "api.toml"))
    if sql_assistant_select == "SQL设置":
        st.write("##### SQL设置")
        st.write("")
        col1, col2 = st.columns([0.6, 0.45], gap="large")
        with col1:

            if not st.session_state.get("sql_assistant_connect_config"):
                sql_assistant_connect_config = {}
                sql_assistant_connect_config["url"] = ""
                sql_assistant_connect_config["port"] = 3306
                sql_assistant_connect_config["username"]= ""
                sql_assistant_connect_config["password"]= ""
                sql_assistant_connect_config["database"]= ""
            else:
                sql_assistant_connect_config = st.session_state.sql_assistant_connect_config
            area = st.container(height=520)
            area.write('''##### ```MySQL设置```''')
            area.write('')
            mysqlURL = area.text_input("**URL**",value=sql_assistant_connect_config.get("url") )
            sql_assistant_connect_config["url"] = mysqlURL
            mysqlPORT = area.number_input("**PORT：**", value=int(sql_assistant_connect_config.get("port",3306)))
            sql_assistant_connect_config["port"] = mysqlPORT
            mysqlUSERNAME = area.text_input("**USERNAME：**", value=sql_assistant_connect_config.get("username"))
            sql_assistant_connect_config["username"] = mysqlUSERNAME
            mysqlPASSWORD = area.text_input("**PASSWORD：**", type="password",value=sql_assistant_connect_config.get("password"))
            sql_assistant_connect_config["password"] = mysqlPASSWORD
            mysqlDataBase = area.text_input("**DATABASE：**", value=sql_assistant_connect_config.get("database"))
            sql_assistant_connect_config["database"] = mysqlDataBase
            # 将状态存储一下（这里已经存储了，就不需要处理了）
            st.session_state.sql_assistant_connect_config = sql_assistant_connect_config
        with col2:
            area2 = st.container(height=450)
            with area2:
                sac.alert(label='Tips',
                          description='当前版本仅支持MySQL，支持版本5.7x,8.x后续支持更多版本！',
                          color='teal',
                          banner=False,
                          icon=True, closable=True)
                sac.alert(label='Tips',
                          description='ＰＯＷＥＲ　ＢＹ　ＨＵＴＥＲＯＸ',
                          color='teal',
                          banner=False,
                          icon=True, closable=True)

        st.write("")
        if st.button('连接测试', use_container_width=True, type="primary"):
            sql_assistant_connect_config = st.session_state.sql_assistant_connect_config
            sqlAssistantHelper = SqlAssistantHelper(**sql_assistant_connect_config)

            if sqlAssistantHelper.connect():
                with area2:
                    sac.alert(label='Tips',
                              description='连接成功',
                              color='teal',
                              banner=False,
                              icon=True, closable=True)

            else:
                sac.alert(label='Tips',
                          description='连接失败',
                          color='yellow',
                          banner=False,
                          icon=True, closable=True)
            # 这里测试连接之后保存一下
            st.session_state.sqlAssistantHelper = sqlAssistantHelper


    if sql_assistant_select == "SQL助手":
        """
        加载配置，并且将其保存在st的session当中
        """
        # 在这里我们先初始化拿到SQLHelper再说
        if st.session_state.get("sqlAssistantHelper"):
            sqlAssistantHelper = st.session_state.sqlAssistantHelper
            st.session_state["sql_assistant_current_sql_connect"]=sqlAssistantHelper.connect()
        else:
            sql_assistant_connect_config = st.session_state.sql_assistant_connect_config
            sqlAssistantHelper = SqlAssistantHelper(**sql_assistant_connect_config)
            st.session_state["sql_assistant_current_sql_connect"]=sqlAssistantHelper.connect()
            st.session_state.sqlAssistantHelper = sqlAssistantHelper

        sql_assistant_c0,sql_assistant_c1,sql_assistant_c2 = st.columns([0.22,0.8,0.4])

        with sql_assistant_c0:
            # 设置当前询问sql数据的时候需要什么模式（全局模式，就是把整个数据库作为预料，反正就是选中哪个就哪个）
            st.session_state["sql_assistant_query_model"] = sac.switch(
                label='全局模式', align='center', size='md',
                value=st.session_state.get("sql_assistant_query_model",True),
            )
            # 在这里展示出我们当前的数据库有哪些表
            table_list: list[str] = sqlAssistantHelper.get_all_tables()
            table_list_container = st.container(height=450)
            with table_list_container:
                current_select_table_name = sac.segmented(
                    items=[
                        sac.SegmentedItem(label=table) for table in table_list
                    ], align='center', direction="vertical",size=11
                )
                st.session_state.current_select_table_name = current_select_table_name
            # 养成好习惯，用完就关
            sqlAssistantHelper.close_connection()

        with sql_assistant_c1:
            # sql助手
            sql_chat_assistant(st,config)

        with sql_assistant_c2:
            st.markdown("###### `关系表图：`")
            current_select_table_name = st.session_state.current_select_table_name
            if current_select_table_name:
                # 展示当前选定的表的关系图
                table_nodes = []
                # 添加节点

                refer_nodes = sqlAssistantHelper.get_table_dependencies(current_select_table_name)
                all_nodes = refer_nodes[::]
                all_nodes.append(current_select_table_name)
                refer_nodes = list(set(refer_nodes))
                all_nodes = list(set(all_nodes))

                for node in all_nodes:
                    table_nodes.append(
                        Node(id=node,
                             label=node,
                             size=8, shape="square")
                    )
                # 添加边
                table_edges = []
                for node in refer_nodes:
                    table_edges.append(
                        Edge(source=current_select_table_name,
                             label="reference",
                             size=8,
                             target=node,
                             )
                    )
                # 定义展示图
                table_config = Config(height=430,
                                      width=250,
                                      nodeHighlightBehavior=True,
                                      highlightColor="#F7A7A6",
                                      directed=True,
                                      collapsible=True)

                table_config_return_value = agraph(nodes=table_nodes,
                                                   edges=table_edges,
                                                   config=table_config)
            else:
                sac.alert(label='Tips',
                          description='空空如也',
                          color='teal',
                          banner=False,
                          icon=True, closable=True)
            # 这里看看能不能正常连接数据库
            if not st.session_state.get("sql_assistant_current_sql_connect"):
                sac.alert(label='Tips',
                          description='数据库连接异常，请查看网络及数据库配置',
                          color='yellow',
                          banner=False,
                          icon=True, closable=True)



    sac.divider(label='POWERED BY @Huterox', icon="lightning-charge", align='center', color='gray', key="5")

