# -*- coding: utf-8 -*-
# @文件：support.py
# @时间：2024/8/14 17:31
# @作者：Huterox
# @邮箱：3139541502@qq.com
# -------------------------------

import asyncio
import json
import logging
from copy import deepcopy
from dataclasses import asdict
import janus
import janus
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lagent.schema import AgentStatusCode
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from webui.handler.search import init_agent



app = FastAPI(docs_url='/')

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

@app.get("/")
def hello():
    return {"message": "Hello, World!"}
@app.post('/solve')
async def run(inputs):
    def convert_adjacency_to_tree(adjacency_input, root_name):
        def build_tree(node_name):
            node = {'name': node_name, 'children': []}
            if node_name in adjacency_input:
                for child in adjacency_input[node_name]:
                    child_node = build_tree(child['name'])
                    child_node['state'] = child['state']
                    child_node['id'] = child['id']
                    node['children'].append(child_node)
            return node

        return build_tree(root_name)

    async def generate():
        try:
            queue = janus.Queue()
            stop_event = asyncio.Event()

            # Wrapping a sync generator as an async generator using run_in_executor
            def sync_generator_wrapper():
                try:
                    for response in agent.stream_chat(inputs):
                        queue.sync_q.put(response)
                except Exception as e:
                    logging.exception(
                        f'Exception in sync_generator_wrapper: {e}')
                finally:
                    # Notify async_generator_wrapper that the data generation is complete.
                    queue.sync_q.put(None)

            async def async_generator_wrapper():
                loop = asyncio.get_event_loop()
                loop.run_in_executor(None, sync_generator_wrapper)
                while True:
                    response = await queue.async_q.get()
                    if response is None:  # Ensure that all elements are consumed
                        break
                    yield response
                    if not isinstance(
                            response,
                            tuple) and response.state == AgentStatusCode.END:
                        break
                stop_event.set()  # Inform sync_generator_wrapper to stop

            async for response in async_generator_wrapper():
                if isinstance(response, tuple):
                    agent_return, node_name = response
                else:
                    agent_return = response
                    node_name = None
                origin_adj = deepcopy(agent_return.adjacency_list)
                adjacency_list = convert_adjacency_to_tree(
                    agent_return.adjacency_list, 'root')
                assert adjacency_list[
                    'name'] == 'root' and 'children' in adjacency_list
                agent_return.adjacency_list = adjacency_list['children']
                agent_return = asdict(agent_return)
                agent_return['adj'] = origin_adj
                response_json = json.dumps(dict(response=agent_return,
                                                current_node=node_name),
                                           ensure_ascii=False)
                yield {'data': response_json}
                # yield f'data: {response_json}\n\n'
        except Exception as exc:
            msg = 'An error occurred while generating the response.'
            logging.exception(msg)
            response_json = json.dumps(
                dict(error=dict(msg=msg, details=str(exc))),
                ensure_ascii=False)
            yield {'data': response_json}
            # yield f'data: {response_json}\n\n'
        finally:
            await stop_event.wait(
            )  # Waiting for async_generator_wrapper to stop
            queue.close()
            await queue.wait_closed()
    agent = init_agent()
    return EventSourceResponse(generate())

def start_support_service():
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8002, log_level='info')


# if __name__ == '__main__':
#     start_support_service