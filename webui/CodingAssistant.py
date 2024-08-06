"""
@FileName：CodingAssistant.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/20 15:44
@Copyright：©2018-2024 awesome!
"""

import toml
from base import current_dir_root
from pluings.languageParse.typeLink import build_link_map, get_link_file
from streamlit_agraph import agraph, Node, Edge, Config
from webui.handler.assistantHandler import *
from webui.handler.assistantHandler import exclude_file_name,exclude_directories


def del_link_file_item(linked_node,current_select_fileItem,show_code_linked_item_tips_container):
    st.session_state.current_link_file_item.remove(linked_node)
    with show_code_linked_item_tips_container:
        with show_code_linked_item_tips_container:
            st.markdown(f'删除关联：`{linked_node.name}`')
    # 记录一下改变的值
    current_link_file_item_change = {"item":current_select_fileItem,"links":st.session_state.current_link_file_item}
    st.session_state.current_link_file_item_change = current_link_file_item_change

def add_link_file_item(linked_node,current_select_fileItem,show_code_linked_item_tips_container):
    if linked_node == current_select_fileItem:
        return
    # 这里对添加的要去重
    t:list = st.session_state.current_link_file_item
    t.append(linked_node)
    st.session_state.current_link_file_item = list(set(t))
    with show_code_linked_item_tips_container:
        st.markdown(f'添加关联：`{linked_node.name}`')
    # 记录一下改变的值
    current_link_file_item_change = {"item":current_select_fileItem,"links":st.session_state.current_link_file_item}
    st.session_state.current_link_file_item_change = current_link_file_item_change

def show_code_linked_item_add(select_add_delete,current_select_fileItem,show_code_linked_item_tips_container):
    with select_add_delete:
        # 通过current_file_map 拿到 fileItem
        current_file_map = st.session_state.current_file_map
        current_file_items = [item for item in current_file_map.values()]
        for linked_node in current_file_items:
            st.checkbox(linked_node.name,on_change=add_link_file_item,args=(linked_node,current_select_fileItem,show_code_linked_item_tips_container,))


def show_code_linked_item_delete(select_add_delete,current_select_fileItem,show_code_linked_item_tips_container):
    with select_add_delete:
        for linked_node in st.session_state.current_link_file_item:
            st.checkbox(linked_node.name,on_change=del_link_file_item,args=(linked_node,current_select_fileItem,show_code_linked_item_tips_container,))


@st.experimental_dialog('代码依赖关系')
def show_code_linked_item(current_select_fileItem):

    show_code_linked_item_tips_container = st.container(height=50)
    linked_file_nodes = [Node(id=current_select_fileItem.name,
                              label=current_select_fileItem.name,
                              size=15, shape="circular")]
    # 添加节点
    for linked_node in st.session_state.current_link_file_item:
        linked_file_nodes.append(
            Node(id=linked_node.name,
                 label=linked_node.name, size=15,
                 shape="circular")
        )
    # 添加边
    linked_file_edges = []
    for linked_node in st.session_state.current_link_file_item:
        linked_file_edges.append(
            Edge(source=current_select_fileItem.name,
                 label="dependent",
                 size=15,
                 target=linked_node.name,
                 )
        )
    # 定义展示图
    file_linked_config = Config(height=280,
                                width=400,
                                nodeHighlightBehavior=True,
                                highlightColor="#F7A7A6",
                                directed=True,
                                collapsible=True)

    file_linked_config_return_value = agraph(nodes=linked_file_nodes,
                                             edges=linked_file_edges,
                                             config=file_linked_config)
    show_code_linked_c0,_,_,_,show_code_linked_c1 = st.columns(5)
    select_add_delete = st.container(height = 80)
    with show_code_linked_c0:
        if st.button("添加",type="primary"):
            show_code_linked_item_add(select_add_delete,current_select_fileItem,show_code_linked_item_tips_container)

    with show_code_linked_c1:
        if st.button("删除",type="primary"):
            show_code_linked_item_delete(select_add_delete,current_select_fileItem,show_code_linked_item_tips_container)


@st.experimental_dialog('添加文件扩展')
def add_include_file_extensions():

    extension_container = st.container(height=300)
    st.text_input(
        label='添加文件扩展',key="add_extension")
    if(st.session_state.get("add_extension")):
        st.session_state.include_file_extensions.add(st.session_state.get("add_extension"))
    with extension_container:
        sac.segmented(
            items=[
                sac.SegmentedItem(label=extension)
                for extension in st.session_state.include_file_extensions
            ],
            label='已允许文件扩展',
            align='center',
            direction="vertical",
            radius='lg', use_container_width=True,
        )

@st.experimental_dialog('解析项目目录',)
def analysis_project(project_path):

    analysis_project_container = st.container(height=300)

    with analysis_project_container:
        sac.alert(label='Tips',
                  description='正在解析项目目录',
                  color='teal',
                  banner=False,
                  icon=True, closable=True)
        try:
            root = get_project_struct(project_path)
            # 将结果存进去：current_project_struct
            st.session_state.current_project_struct = root
            st.session_state["current_project_path"] = project_path
            sac.alert(label='Tips',
                      description='项目目录解析完毕',
                      color='teal',
                      banner=False,
                      icon=True, closable=True)

        except Exception as e:
            print(e)
            sac.alert(label='Wanning',
                      description='项目目录解析失败⚓',
                      banner=False,
                      color='yellow',
                      icon=True, closable=True)

def assistantUI():

    global exclude_directories
    global exclude_file_name

    st.subheader("MathAI V0.1")
    st.caption("POWERED BY @Huterox")
    config = toml.load(os.path.join(current_dir_root, "api.toml"))
    assistant_select = sac.tabs([
        sac.TabsItem(label='对话模式', icon='lightning'),
        sac.TabsItem(label='项目问答', icon='yin-yang')
    ], align='center', variant='outline', use_container_width=True, index=0)

    if assistant_select == "对话模式":
        code_assistant(st,config)
    if assistant_select == "项目问答":
        col1, col2 = st.columns([0.4, 0.6], gap="large")
        """
        col1 是左侧上传项目文件
        col2 是对话框，在左侧完成操作之后，右侧将获得：current_select_content
        这个是当前的用户上传完毕项目文件之后，选中的代码文件内容，之后我们要对其进行问答处理
        此外，在左侧的操做当中，还会得到当前用户选中的文件：current_select_fileItem
        """
        with col1:
            project_path = st.text_input("请输入项目地址", key="project_path",
                                         on_change=clear_current_project_struct,
                                         value=st.session_state.get("current_project_path"),

                                         )
            # 在这里读取解析到的目录
            if st.session_state.get("current_project_struct"):
                current_project_struct_container = st.container(height=400)
                with current_project_struct_container:
                    root = st.session_state.get("current_project_struct")
                    rootTreeItem = sac.TreeItem(label="default",children=[],tag=[sac.Tag('目录', color='yellow')])
                    # 这里记录了当前的文件名字和对应的FileItem
                    current_file_map = {}
                    rootTreeItem = build_tree(root,rootTreeItem,current_file_map)
                    st.session_state.current_file_map = current_file_map
                    # 构造对应的适配器（用来寻找当前代码相关联的对象）
                    st.session_state.current_link_map = build_link_map(current_file_map)
                    select_file = sac.tree(items=[
                        rootTreeItem
                    ], label='当前项目', index=0, align='center', size='md',
                        color='blue',
                        open_all=True, checkbox_strict=True
                    )
                    # 当前被选中的项目文件
                    current_select_fileItem = st.session_state.current_file_map.get(select_file,"")
                    st.session_state.current_select_fileItem = current_select_fileItem

            else:
                # 这个是给两个按钮的布局
                col11, col22,col33 = st.columns([2,2,0.5], gap="large")
                if (not st.session_state.get("project_path")):
                    sac.alert(label='Wanning',
                              description='请输入项目根路径，并确保目录权限',
                              banner=False,
                              color='yellow',
                              icon=True, closable=True)
                else:
                    sac.alert(label='Tips',
                              description='请点击`解析项目目录`后点击`↻`按钮',
                              color='teal',
                              banner=False,
                              icon=True, closable=True)
                    with col22:
                        if st.button(label='解析项目', type="primary"):
                            analysis_project(st.session_state.get("project_path"))
                    with col33:
                        st.button("↻")
                with col11:
                    if st.button(label='添加拓展', type="primary"):
                        add_include_file_extensions()

        with col2:
            if st.session_state.get("current_project_struct"):
                # 只有当项目目录刷新出来了，才能进行选择，然后进行逻辑处理
                current_select_fileItem = st.session_state.get("current_select_fileItem")
                if current_select_fileItem:
                    # 只有当选中了文件Item才能有相关适配器
                    # 找到关联(先找到当前有没有适配器)
                    current_adapter = st.session_state.current_link_map.get(current_select_fileItem.name)
                    if not current_adapter:
                        sac.alert(label='Tips',
                                  description=f'当前对象暂不支持解析，请选择其他代码文件',
                                  color='yellow',
                                  banner=False,
                                  icon=True, closable=True)
                    else:
                        # 这里在加载当前关联的时候，需要优先以修改过的为主
                        current_link_file_item_change = st.session_state.get("current_link_file_item_change")
                        if current_link_file_item_change and current_link_file_item_change.get("item") == current_select_fileItem:
                            current_link_file_item = current_link_file_item_change.get("links")
                            st.session_state.current_link_file_item = current_link_file_item
                        else:
                            current_link_file_item = get_link_file(current_adapter,st.session_state.current_link_map)
                            # 将当前这个文件的链接文件存储进入到状态当中，方便在别的地方拿到
                            st.session_state.current_link_file_item = list(set(current_link_file_item))
                        # for item in current_link_file_item:
                        #     print(item.name)
                if current_select_fileItem:
                    # sac.alert(label='Tips',
                    #           description=f'当前选中的文件是：{current_select_fileItem.name}',
                    #           color='teal',
                    #           banner=False,
                    #           icon=True, closable=True)
                    # 这里的话，就不展示文件名字了，直接展示选中代码文件的关系图
                    # 当前选中的文件节点
                    sac.alert(label='Tips',
                              description=f'点击`查看当前依赖`可编辑当前代码依赖',
                              color='teal',
                              banner=False,
                              icon=True, closable=True)
                    # 在项目问答当中的操作按钮
                    c_d_0,c_d_1,c_d_2 = st.columns(3)
                    with c_d_0:
                        if(st.button("查看当前依赖",type="primary")):
                            show_code_linked_item(current_select_fileItem)


                else:
                    sac.alert(label='Tips',
                              description=f'请选择对应的代码文件进行问答（部分文件暂不支持解析）',
                              color='yellow',
                              banner=False,
                              icon=True, closable=True)

            ##################### 项目问答对话模块 ####################
            # 这里的重点是，拿到当前选中的模块，和相关联的模块，发送LLM进行问答关联
            # 当前这里需要优化的点是，没有对代码段落进行分段处理，而是直接将完整代码给到
            project_assistant(st,config)