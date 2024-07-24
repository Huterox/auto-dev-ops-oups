"""
@FileName：collationHandler.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/24 14:10
@Copyright：©2018-2024 awesome!
"""
import time
import toml
from base import current_dir_root, whisper_tiny_dict
from bot.collection.agents import CollectionSummaryAgent, CollectionQuestionAgent
from pluings.whisper.transUtils import faster_whisper_result

"""
提取解析音频
"""
import os

"""
解析音频的内容
"""
def get_audio_content(audio_file):
    import os
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    video_config = toml.load(os.path.join(current_dir_root, "api.toml"))
    faster_whisper_model = video_config["WHISPER"]["faster_whisper_model_default"]  # faster_whisper配置
    faster_whisper_local = video_config["WHISPER"]["faster_whisper_model_local"]  # 本地模型加载
    # faster_whisper_local_path = video_config["WHISPER"]["faster_whisper_model_local_path"]  # 本地模型路径
    faster_whisper_local_path = whisper_tiny_dict # tiny版本的模型在本地设置当中就写好
    whisper_prompt_setting = video_config["MORE"]["whisper_prompt"]
    temperature_setting = video_config["MORE"]["temperature"]
    gpu_setting = video_config["WHISPER"]["gpu"]
    vad_setting = video_config["WHISPER"]["vad"]
    lang_setting = video_config["WHISPER"]["lang"]
    min_vad_setting = video_config["MORE"]["min_vad"]
    beam_size_setting = video_config["MORE"]["beam_size"]

    device = 'cuda' if gpu_setting else 'cpu'
    model = faster_whisper_model
    if faster_whisper_local:
        model = faster_whisper_local_path

    """
        segments_dict = {
        'text': ' '.join([segment.text for segment in segments]),
        'segments': [{
            'id': segment.id,
            'seek': segment.seek,
            'start': segment.start,
            'end': segment.end,
            'text': segment.text,
            'tokens': segment.tokens,
            'temperature': segment.temperature,
            'avg_logprob': segment.avg_logprob,
            'compression_ratio': segment.compression_ratio,
            'no_speech_prob': segment.no_speech_prob}
            for segment in segments
        ]
    }
    """
    try:
        result = faster_whisper_result(audio_file, device, model, whisper_prompt_setting, temperature_setting,
                                       vad_setting, lang_setting, beam_size_setting, min_vad_setting)

        return result["text"]
    except Exception as e:
        print(e)
        return "抱歉当前语音识别失败😣"

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