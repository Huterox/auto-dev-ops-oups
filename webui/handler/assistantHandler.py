"""
@FileName：assistantHandler.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/20 22:57
@Copyright：©2018-2024 awesome!
"""
import os
import time
from openai import OpenAI
import streamlit as st
import streamlit_antd_components as sac
from webui.handler.dialog import dialog_info


exclude_directories = {
    '.git', '.svn', '.hg', '.tox', 'venv', 'env',
    'node_modules', 'bower_components', 'vendor',
    'target', 'out', 'build', 'dist', '.vscode',
    '.idea', 'logs', 'cache', 'caches', 'bin',
    'obj', 'objd', 'lib', 'libs', 'deps', 'dependencies',
    '__pycache__', '.mypy_cache', '.pytest_cache', '.gitignore',
    '.svnignore', '.hgignore', '.DS_Store', 'Thumbs.db',
    '.directory', 'node_modules/.bin', 'bower_components/.bin',
    '.streamlit'
}

exclude_file_name = {
    '__init__.py'
}

include_file_extensions = {
    ".java",".py",".html",".vue",".js",".ts"
}

"""
先将这些默认的设置加入到streamlit的缓存当中去
"""

st.session_state.exclude_directories = exclude_directories
st.session_state.exclude_file_name = exclude_file_name
st.session_state.include_file_extensions = include_file_extensions

def code_assistant(st,config):
    messages_code_assistant = st.container(height=470)
    if "messages_code_assistant" not in st.session_state:
        st.session_state["messages_code_assistant"] = [
            {"role": "assistant",
             "content": "你好我是MatchAI的代码助手，很高兴能够帮助到您🚓?"}
        ]

    for msg in st.session_state.messages_code_assistant:
        messages_code_assistant.chat_message(msg["role"]).write(msg["content"])

    default_key = config["DEFAULT"]["default_key"]
    default_base = config["DEFAULT"]["default_base"]
    default_model = config["DEFAULT"]["default_model"]
    default_temperature = config["DEFAULT"]["default_temperature"]
    if (default_base != None and default_model != ""):
        placeholder = "有什么我可以帮你的么？😀"
    else:
        placeholder = "有什么我可以帮你的么？😀(请先设置默认大模型KEY)"
    if prompt := st.chat_input(placeholder=placeholder):
        client = OpenAI(api_key=default_key,
                        base_url=default_base,

                        )
        st.session_state.messages_code_assistant.append({"role": "user", "content": prompt})
        messages_code_assistant.chat_message("user").write(prompt)
        response = client.chat.completions.create(
            model=default_model,
            temperature=default_temperature,
            messages=[
                {"role": "system",
                 "content": "你是一个专业的代码专家，你叫Match，精通任何代码，请你帮助用户回答和代码相关的问题。\n"},
                {"role": "user", "content": prompt}
            ])
        msg = response.choices[0].message.content
        st.session_state.messages_code_assistant.append({"role": "assistant", "content": msg})
        with messages_code_assistant.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ''
            for item in msg:
                full_response += item
                time.sleep(0.01)
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
        # messages.chat_message("assistant").write_stream(msg)


"""
在项目对话助手这里，我们需要处理两个东西：
st.session_state.get("current_link_file_item")
st.session_state.get("current_select_fileItem")
我们需要这两个玩意来构建我们的prompt
"""
# 动态构建对应的prompt
def build_assistant_prompt():
    current_link_file_item:list = st.session_state.get("current_link_file_item")
    current_select_fileItem = st.session_state.get("current_select_fileItem")
    dependent = """"""
    for link_item in current_link_file_item:
        dependent+=f"代码文件：{link_item.name}+\n"
        dependent+=f"代码内容：\n```\n{link_item.content}\n```\n"

    system_prompt = f"""
    你是一个AI助手，你需要结合下面给你的代码来回答用户的问题。下面是我们的代码
    当前查看代码{current_select_fileItem.name}
    代码内容：
    ```
    {current_select_fileItem.content}
    ```
    对应的依赖代码
    {dependent}
    ---------
    请你按照上面的代码内容来回答用户的问题。
    """
    return system_prompt

# 项目助手(这里需要注意的是，我们的prompt上下文需要实时变动)
def project_assistant(st,config):
    # 项目助手对应的聊天容器
    project_assistant_messages = st.container(height=470)
    if "project_assistant_messages" not in st.session_state:
        st.session_state["project_assistant_messages"] = [
            {"role": "assistant", "content": "你好我是MatchAI的项目代码助手，很高兴能够帮助到您🚓！"}
        ]

    # 项目助手对话的记录
    for msg in st.session_state.project_assistant_messages:
        project_assistant_messages.chat_message(msg["role"]).write(msg["content"])

    # 拿到LLM相关的设置
    default_key = config["DEFAULT"]["default_key"]
    default_base = config["DEFAULT"]["default_base"]
    default_model = config["DEFAULT"]["default_model"]
    default_temperature = config["DEFAULT"]["default_temperature"]
    if(default_base!=None and default_model!=""):
        placeholder = "有什么我可以帮你的么？😀"
    else:
        placeholder = "有什么我可以帮你的么？😀(请先设置默认大模型KEY)"

    # 如果当前可以拿到当前选中的文件的Item（是支持的，那么我们就可以正常执行）
    if st.session_state.get("current_link_file_item"):
        if prompt := st.chat_input(placeholder=placeholder):
            client = OpenAI(api_key=default_key,
                            base_url=default_base,

                            )
            # 添加用户的对话记录
            st.session_state.project_assistant_messages.append({"role": "user", "content": prompt})
            # 在容器当中展示用户的对话
            project_assistant_messages.chat_message("user").write(prompt)
            response = client.chat.completions.create(
                model=default_model,
                temperature=default_temperature,
                messages=[
                    {"role": "system",
                     "content": build_assistant_prompt()},
                    {"role": "user", "content": prompt}
                ])
            msg = response.choices[0].message.content
            # 添加模型返回结果（在对话记录当中）
            st.session_state.project_assistant_messages.append({"role": "assistant", "content": msg})
            # 在对话容器添加对应的响应内容
            with project_assistant_messages.chat_message("assistant"):
                placeholder = st.empty()
                full_response = ''
                for item in msg:
                    full_response += item
                    time.sleep(0.01)
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
            # messages.chat_message("assistant").write_stream(msg)
    else:
        # 这里的提示不加入历史对话记录当中去
        with project_assistant_messages.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ''
            msg = "请选择对应的项目文件进行对话哦~如果您有任何疑问请前往【首页】询问小助手😄"
            for item in msg:
                full_response += item
                time.sleep(0.01)
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)

def filter_directories(dir_name: str):
    for file in st.session_state.exclude_directories:
        if file == dir_name:
            return True
    return False

def filter_file_name(dir_name: str):
    for file in st.session_state.exclude_file_name:
        if file == dir_name:
            return False
    return True

def filter_allow_file(file_name: str):
    for file in st.session_state.include_file_extensions:
        if file == "." + file_name.split(".")[-1]:
            return True
    return False

class FileItem(object):
    def __init__(self):
        # 文件名字
        self.name = ''
        # 文件路径
        self.path = ''
        # 子文件（一般是文件夹才有）
        self.children = []
        # 是不是文件夹
        self.is_dir = False
        # 文件类型
        self.type = ""
        # 文件内容（方便关联到依赖）
        self.content = ""

    def __str__(self) -> str:
        return f"{self.name} " \
               f"{self.path} " \
               f"{self.is_dir} " \
               f"{self.type} " \
               f"content len:{len(self.content)}"

    def __eq__(self, other):
        if isinstance(other, FileItem):
            return self.name == other.name and self.path == other.path and self.is_dir == other.is_dir and self.type == other.type
        return False


"""
从当前的跟目录出发，得到一个完整的文档树
"""
def get_project_struct(project_path):
    if not os.path.exists(project_path) and not os.path.isdir(project_path):
        dialog_info("提供的项目路径不存在或提供的不是目录")
        return "提供的项目路径不存在或提供的不是目录"
    # 开始递归处理
    def recurse_directories(path,root):

        if os.path.isdir(path):
            # 如果是目录就往下搜索
            root.name = path.split(os.path.sep)[-1]
            root.is_dir = True
            root.path = path
            items = os.listdir(path)
            # 处理当前目录的下级
            for item in items:
                node = FileItem()
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    # 过滤一些不需要的文件夹
                    if (not filter_directories(item)):
                        root.children.append(recurse_directories(full_path,node))

                else:
                    if filter_allow_file(full_path):
                        node.name = os.path.basename(full_path)
                        # 要在允许的文件当中才行
                        if filter_file_name(node.name):
                            node.is_dir = False
                            node.path = full_path
                            node.type = full_path.split(".")[-1]
                            with open(full_path, 'r',encoding='utf-8') as f:
                                node.content = f.read()
                            root.children.append(node)

        return root
    root = FileItem()
    recurse_directories(project_path, root)
    return root

def build_tree(root,rootTreeItem,current_file_map):
    # 这里可以保证，root 第一个节点一定是文件夹
    rootTreeItem.label = root.name
    for child in root.children:
        if(child.is_dir):
            rootTreeItem.children.append(
                build_tree(child,sac.TreeItem(label=child.name,
                                              children=[],
                                              disabled=True,
                                              tag=[sac.Tag('目录', color='yellow')]),current_file_map)
            )
        else:

            rootTreeItem.children.append(
                sac.TreeItem(label=os.path.basename(child.path),
                             children=[],
                             tag=[sac.Tag(child.type, color='cyan')])
            )
            # 这里记录一下所有的项目文件（符合条件的）
            current_file_map[os.path.basename(child.path)] = child
    return rootTreeItem

# 情况当前项目的缓存
def clear_current_project_struct():

    # 清空当前的项目结构
    st.session_state["current_project_struct"] = None
    # 清空当前的相关缓存
    st.session_state["current_select_fileItem"] = None


if __name__ == '__main__':
    node = get_project_struct(r"F:\projects\MatchPro\AutoDevOps-oups")
    print(node)