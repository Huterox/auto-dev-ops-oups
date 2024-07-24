"""
@FileName：collationHandler.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/24 14:10
@Copyright：©2018-2024 awesome!
"""
import time
from bot.collection.agents import CollectionSummaryAgent, CollectionQuestionAgent


"""
Get the summary of requirements by use the agent of CollectionSummaryAgent
"""

def container_bot_write(st,container,key,value):
    # writen the key with value in session state
    st.session_state[key] = value
    # with the container to show the component
    # with container.chat_message("assistant"):
    #     placeholder = st.empty()
    #     full_response = ''
    #     for item in value:
    #       full_response += item
    #       time.sleep(0.005)
    #       placeholder.markdown(full_response)
    #     placeholder.markdown(full_response)

def getCollectionSummary(st,collation_summary_container,history):
    # check the switch is open
    summary = ""
    if st.session_state.get("collation_summary_open",False):
        if history==None or history==[]:
            summary = "您还未输入任何内容，无法生成需求总结"
        else:
            agent = CollectionSummaryAgent()
            summary = agent.get_summary(history)
    else:
        summary = "您并未开启次功能，是否开启？体验智能需求总结？"
    # to write the summary in the container to show
    container_bot_write(st,collation_summary_container, "collation_summary_content", summary)
    return summary


def getCollectionSuggest(st,collation_suggest_container,history):
    # check the switch is open
    suggest = ""
    if st.session_state.get("collation_suggest_open",False):
        if history==None or history==[]:
            suggest = "您还未输入任何内容，无法生成智能建议"
        else:
            agent = CollectionQuestionAgent()
            suggest = agent.get_suggest(history)
    else:
        suggest = "您并未开启次功能，是否开启？体验智能建议？"
    # to write the summary in the container to show
    container_bot_write(st,collation_suggest_container, "collation_suggest_content", suggest)
    return suggest