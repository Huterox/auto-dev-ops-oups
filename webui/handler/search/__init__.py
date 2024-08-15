# -*- coding: utf-8 -*-
# @文件：__init__.py
# @时间：2024/8/14 15:53
# @作者：Huterox
# @邮箱：3139541502@qq.com
# -------------------------------
import toml
from lagent import GPTAPI

from base import mylogger, current_dir_root

mylogger.info("loading search module......")
import os
from datetime import datetime

from lagent.actions import ActionExecutor, BingBrowser


from webui.handler.search.search_agent import (MindSearchAgent,
                                               MindSearchProtocol)
from webui.handler.search.search_prompt import (
    FINAL_RESPONSE_CN,  GRAPH_PROMPT_CN,
    fewshot_example_cn, graph_fewshot_example_cn,
     searcher_context_template_cn,
     searcher_input_template_cn,
    searcher_system_prompt_cn,
  )

LLM = {}


"""
初始化得到Agent
"""
def init_agent():

    config = toml.load(os.path.join(current_dir_root, "api.toml"))
    default_key = config["DEFAULT"]["default_key"]
    default_base = config["DEFAULT"]["default_base"]
    default_model = config["DEFAULT"]["default_model"]
    default_temperature = config["DEFAULT"]["default_temperature"]
    bing_api_key = config["DEFAULT"]["bing_api_key"]
    llm = GPTAPI(model_type=default_model, key=default_key,openai_api_base=default_base)
    interpreter_prompt = GRAPH_PROMPT_CN
    plugin_prompt = searcher_system_prompt_cn

    agent = MindSearchAgent(
        llm=llm,
        protocol=MindSearchProtocol(meta_prompt=datetime.now().strftime(
            'The current date is %Y-%m-%d.'),
                                    interpreter_prompt=interpreter_prompt,
                                    response_prompt=FINAL_RESPONSE_CN
                                    ),
        searcher_cfg=dict(
            llm=llm,

            plugin_executor=ActionExecutor(
                BingBrowser(searcher_type='DuckDuckGoSearch',
                            topk=6,
                            api_key=bing_api_key)),

            protocol=MindSearchProtocol(
                meta_prompt=datetime.now().strftime(
                    'The current date is %Y-%m-%d.'),
                plugin_prompt=plugin_prompt,
            ),
            template=dict(input=searcher_input_template_cn,
                          context=searcher_context_template_cn
                          )),
        max_turn=10)
    return agent