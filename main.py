import streamlit as st
import streamlit_antd_components as sac
import threading

from base import mylogger
from webui.ChatFlow import chatFlowUI
from webui.Home import homeUI
from webui.RequirementsCollation import collationUI
from webui.CodingAssistant import assistantUI
from webui.AutoDevOps import autoUI
from webui.SQLAssistant import sqlAssistantUI
from webui.Search import searchUI
from webui.handler.search.support import start_support_service

st.set_page_config(
    page_title="MatchAI-智码 v0.1",
    page_icon=":material/radio_button_checked:",
    layout="wide",  # 设置布局样式为宽展示
    initial_sidebar_state="expanded"  # 设置初始边栏状态为展开
)

with st.sidebar.container():
    st.subheader("MatchAI-智码 v0.1")
    menu = sac.menu(
        items=[
            sac.MenuItem('首页', icon='house-fill'),
            sac.MenuItem('编码助手', icon='robot', children=[
                sac.MenuItem('项目分析', icon='chat-left-text'),
                sac.MenuItem('Search🔍', icon='search'),
                sac.MenuItem('SQL助手', icon='filetype-sql'),
                sac.MenuItem('需求分析', icon='file-earmark-break'),
            ]),
            sac.MenuItem('系统生成', icon='alt', children=[
                sac.MenuItem('Auto流程', icon='fan'),
                sac.MenuItem('ChatFlow', icon='hourglass'),
            ]),
        ],
        key='menu',
        color='blue',
        open_index=[1, 2]
    )
    sac.divider(label='POWERED BY @Huterox', icon="lightning-charge", align='center', color='gray')

if __name__ == '__main__':
    menus_page = {
        "首页": homeUI,
        "项目分析": assistantUI,
        "Search🔍": searchUI,
        "SQL助手": sqlAssistantUI,
        "需求分析": collationUI,
        "Auto流程": autoUI,
        "ChatFlow": chatFlowUI
    }

    with st.sidebar:
        sac.buttons(items=[
            sac.ButtonsItem(label='Blog主页！', icon='send',
                            href='https://blog.csdn.net/FUTEROX?spm=1000.2115.3001.5343')],
            variant='dashed', index=None, direction='vertical',
            use_container_width=True, align='center', color='dark'
        )

    custom_css = """
            <style>
            #MainMenu {visibility: hidden;}
            .st-emotion-cache-1wbqy5l.e17vllj40 {visibility: hidden;}
            .st-emotion-cache-1i41fkg.e1f1d6gn2{
                height: 600px;
                overflow-y: scroll; /* 添加垂直滚动条 */
            }
            </style>
        """
    st.markdown(custom_css, unsafe_allow_html=True)
    with st.container():
        menus_page.get(menu)()

    if not st.session_state.get("open_support_service", False):
        # 默认开启服务
        mylogger.info("opening the support service for search")
        t = threading.Thread(target=start_support_service)
        t.start()
        st.session_state["open_support_service"] = True
