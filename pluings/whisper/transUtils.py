"""
@FileName：transUtils.py
@Author：Huterox
@Description：Go For It
@Time：2024/6/30 19:10
@Copyright：©2018-2024 awesome!
"""

import os
import re
import math
import time
import json
import requests
import anthropic
import subprocess
import pandas as pd
from openai import OpenAI
import google.generativeai as genai
from faster_whisper import WhisperModel

from base import mylogger


def cache(cache):  # 缓存检测
    total_size = 0
    for root, dirs, files in os.walk(cache):  # 遍历文件夹中的所有文件和子文件夹
        for file_name in files:
            file_path = os.path.join(root, file_name)
            total_size += os.path.getsize(file_path)
    return total_size


def convert_size(size):  # 缓存大小匹配
    if size == 0:
        return "0B"
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    power = math.pow(1024, i)
    size = round(size / power, 2)
    return f"{size} {size_names[i]}"

"""
获取文件夹下面的文件夹信息
"""
def get_folders_info(root_folder):
    ind = 1
    folders_info = []
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            folder_size = cache(folder_path)
            folders_info.append({
                '序号': str(ind),
                '文件名': folder_name,
                '大小': convert_size(folder_size)
            })
            ind += 1
    return pd.DataFrame(folders_info)

"""
获取文件夹下面的文件信息
"""
def get_info(root_folder):
    ind = 1
    folders_info = []
    for folder_name in os.listdir(root_folder):
        folder_size = os.path.getsize(root_folder + folder_name)
        folders_info.append({
            '序号': str(ind),
            '文件名': folder_name,
            '大小': convert_size(folder_size)
        })
        ind += 1
    return pd.DataFrame(folders_info)

"""
将文件转化为mp3格式
"""
def file_to_mp3(log, file_name, path):
    try:
        if file_name.split('.')[-1] != "mp3":
            command = f"ffmpeg -loglevel {log} -i {file_name} -vn -acodec libmp3lame -ab 320k -f mp3 output.mp3"
            subprocess.run(command, shell=True, cwd=path)
    except:
        raise EOFError("错误！可能是 FFmpeg 未被正确配置 或 上传文件格式不受支持！")

"""
faster-whisper中生成器转换dict
"""
def faster_whisper_result_dict(segments):
    segments = list(segments)
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
    return segments_dict

"""
使用OpenAI来实现字幕识别
"""
def openai_whisper_result(key, base, path, prompt, temperature):
    print("\n*** OpenAI API 调用模式 ***\n")
    if base != "https://api.openai.com/v1":
        print(f"- 代理已开启，URL：{base}")
    try:
        path.split('.')
        audio_file = open(path, "rb")
    except:
        audio_file = open(path + "/output.mp3", "rb")

    client = OpenAI(api_key=key, base_url=base)
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["segment"],
        prompt=prompt,
        temperature=temperature)
    result = {'text': transcript.text, 'segments': transcript.segments}
    print(f"- whisper识别内容：\n{result['text']}\n")
    return result

"""
使用faster_whisper来实现字幕识别
注意这里支持的模型有：
'tiny', 'tiny.en', 
'base', 'base.en', 
'small', 'small.en', 
'medium', 'medium.en', 
'large-v1','large-v2', 'large-v3', 'large', 
'distil-small.en', 'distil-medium.en', 'distil-large-v2','distil-large-v3'                
"""
def faster_whisper_result(file_path, device, model_name, prompt, temp, vad, lang, beam_size, min_vad):
    if model_name not in ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large-v1',
                          'large-v2', 'large-v3', 'large', 'distil-small.en', 'distil-medium.en', 'distil-large-v2',
                          'distil-large-v3']:
        print("\n*** Faster Whisper 本地模型加载模式 ***\n")
    else:
        print("\n*** Faster Whisper 调用模式 ***\n")

    mylogger.info(f"- 运行模型：{model_name}")
    mylogger.info(f"- 运行方式：{device}")
    mylogger.info(f"- VAD辅助：{vad}")

    try:
        file_path.split('.')
        file_path = open(file_path, "rb")
    except:
        file_path = open(file_path + "/output.mp3", "rb")

    model = WhisperModel(model_name, device)
    if lang == "自动识别" and vad is False:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       beam_size=beam_size,
                                       temperature=temp
                                       )
    elif lang == "自动识别" and vad is True:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       beam_size=beam_size,
                                       vad_filter=vad,
                                       vad_parameters=dict(min_silence_duration_ms=min_vad),
                                       temperature=temp
                                       )
    elif vad is False:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       language=lang,
                                       beam_size=beam_size,
                                       temperature=temp
                                       )
    elif vad is True:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       language=lang,
                                       beam_size=beam_size,
                                       vad_filter=vad,
                                       vad_parameters=dict(min_silence_duration_ms=min_vad),
                                       temperature=temp
                                       )

    result = faster_whisper_result_dict(segments)
    mylogger.info(f"- whisper识别内容：\n{result['text']}\n")
    return result

"""
使用在线的大语言模型来进行翻译，接收srt，需要取到srt内容（额外进行解析）
"""
def translate(system_prompt, user_prompt, api_key, base_url, model, result, wait_time, srt):
    if "gpt" in model:
        if base_url != "https://api.openai.com/v1":
            mylogger.info(f"- 代理地址：{base_url}")
        mylogger.info("- 翻译内容：\n")
        client = OpenAI(api_key=api_key, base_url=base_url)
        segment_id = 0
        segments = result['segments']
        for segment in segments:
            text = segment['text']
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt + str(text)}
                ])
            answer = response.choices[0].message.content
            if srt == "原始语言为首":
                result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
            elif srt == "目标语言为首":
                result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
            else:
                result['segments'][segment_id]['text'] = answer
            segment_id += 1
            mylogger.info(answer)
            time.sleep(wait_time)

    elif "claude" in model:
        if base_url != "https://api.anthropic.com/v1/messages":
            mylogger.info(f"- 代理地址：{base_url}")
        mylogger.info("- 翻译内容：\n")
        segment_id = 0
        segments = result['segments']
        for segment in segments:
            text = segment['text']
            client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
            message = client.messages.create(
                model=model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt + str(text)}
                ])
            answer = message.content[0]['text']
            if srt == "原始语言为首":
                result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
            elif srt == "目标语言为首":
                result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
            else:
                result['segments'][segment_id]['text'] = answer
            segment_id += 1
            mylogger.info(answer)
            time.sleep(wait_time)

    elif "gemini" in model:
        mylogger.info("- 翻译内容：\n")
        if base_url is None:
            mylogger.info("- Python SDK 调用（若想使用代理，请填入对应的BASE_URL后自动使用代理模式！)")
            segment_id = 0
            segments = result['segments']
            for segment in segments:
                text = segment['text']
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model)
                answer = model.generate_content(user_prompt + str(text))
                if srt == "原始语言为首":
                    result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
                elif srt == "目标语言为首":
                    result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
                else:
                    result['segments'][segment_id]['text'] = answer
                segment_id += 1
                mylogger.info(answer.text)
                time.sleep(wait_time)
        else:
            mylogger.info("- Request 请求调用（适用于代理模式，若不想使用Request模式，请把BASE_URL留空！)")
            mylogger.info(f"- **Beta** 代理地址：{base_url}\n")
            segment_id = 0
            segments = result['segments']
            for segment in segments:
                text = segment['text']
                payload = json.dumps({
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_prompt + str(text)
                        }
                    ],
                    "temperature": 0.8
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': api_key
                }
                response = requests.request("POST", base_url, headers=headers, data=payload)
                answer = response.json()
                try:
                    answer = answer["choices"][0]["message"]["content"]
                    if srt == "原始语言为首":
                        result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
                    elif srt == "目标语言为首":
                        result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
                    else:
                        result['segments'][segment_id]['text'] = answer
                    segment_id += 1
                    mylogger.info(answer.text)
                    time.sleep(wait_time)
                except Exception as e:
                    mylogger.info("-------请阅读下方报错内容------\n")
                    mylogger.info(f"An error occurred: {type(e).__name__}, with message: \n {answer}")
                    mylogger.info("\n-------请根据报错检查你的key或者代理-------\n")
                    raise e

    else:
        mylogger.info("- 翻译内容：\n")
        client = OpenAI(api_key=api_key, base_url=base_url)
        segment_id = 0
        segments = result['segments']
        for segment in segments:
            text = segment['text']
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt + str(text)}
                ])
            answer = response.choices[0].message.content
            if srt == "原始语言为首":
                result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
            elif srt == "目标语言为首":
                result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
            else:
                result['segments'][segment_id]['text'] = answer
            segment_id += 1
            mylogger.info(answer)
            time.sleep(wait_time)
    return result

"""
使用外部的大语言模型来进行翻译
"""
def translate_srt(system_prompt, user_prompt, api_key, base_url, model, srt_content, wait_time, srt):
    if "gpt" in model:
        if base_url != "https://api.openai.com/v1":
            mylogger.info(f"- 代理地址：{base_url}")
        mylogger.info("- 翻译内容：\n")
        client = OpenAI(api_key=api_key, base_url=base_url)
        segment_id = 0
        for segment in srt_content:
            text = segment['text']
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt + str(text)}
                ])
            answer = response.choices[0].message.content
            if srt == "原始语言为首":
                srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
            elif srt == "目标语言为首":
                srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
            else:
                srt_content[segment_id]['text'] = answer
            segment_id += 1
            mylogger.info(answer)
            time.sleep(wait_time)

    elif "claude" in model:
        if base_url != "https://api.anthropic.com/v1/messages":
            mylogger.info(f"- 代理地址：{base_url}")
        mylogger.info("- 翻译内容：\n")
        segment_id = 0
        for segment in srt_content:
            text = segment['text']
            client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
            message = client.messages.create(
                model=model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt + str(text)}
                ])
            answer = message.content[0]['text']
            if srt == "原始语言为首":
                srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
            elif srt == "目标语言为首":
                srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
            else:
                srt_content[segment_id]['text'] = answer
            segment_id += 1
            mylogger.info(answer)
            time.sleep(wait_time)

    elif "gemini" in model:
        mylogger.info("- 翻译内容：\n")
        if base_url is None:
            mylogger.info("- Python SDK 调用（若想使用代理，请填入对应的BASE_URL后自动使用代理模式！)")
            segment_id = 0
            for segment in srt_content:
                text = segment['text']
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model)
                answer = model.generate_content(user_prompt + str(text))
                if srt == "原始语言为首":
                    srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
                elif srt == "目标语言为首":
                    srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
                else:
                    srt_content[segment_id]['text'] = answer
                segment_id += 1
                mylogger.info(answer.text)
                time.sleep(wait_time)
        else:
            mylogger.info("- Request 请求调用（适用于代理模式，若不想使用Request模式，请把BASE_URL留空！)")
            mylogger.info(f"- **Beta** 代理地址：{base_url}\n")
            segment_id = 0
            for segment in srt_content:
                text = segment['text']
                payload = json.dumps({
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_prompt + str(text)
                        }
                    ],
                    "temperature": 0.8
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': api_key
                }
                response = requests.request("POST", base_url, headers=headers, data=payload)
                answer = response.json()
                try:
                    answer = answer["choices"][0]["message"]["content"]
                    if srt == "原始语言为首":
                        srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
                    elif srt == "目标语言为首":
                        srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
                    else:
                        srt_content[segment_id]['text'] = answer
                    segment_id += 1
                    mylogger.info(answer.text)
                    time.sleep(wait_time)
                except Exception as e:
                    mylogger.info("-------请阅读下方报错内容------\n")
                    mylogger.info(f"An error occurred: {type(e).__name__}, with message: \n {answer}")
                    mylogger.info("\n-------请根据报错检查你的key或者代理-------\n")
                    raise e

    else:
        mylogger.info("- 翻译内容：\n")
        client = OpenAI(api_key=api_key, base_url=base_url)

        segment_id = 0
        for segment in srt_content:
            text = segment['text']
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt + str(text)}
                ])
            answer = response.choices[0].message.content
            if srt == "原始语言为首":
                srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
            elif srt == "目标语言为首":
                srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
            else:
                srt_content[segment_id]['text'] = answer
            segment_id += 1
            mylogger.info(answer)
            time.sleep(wait_time)
    return srt_content

"""
使用本地的大语言模型来进行翻译，接收srt，需要取到srt内容（额外进行解析）
"""
def local_translate(system_prompt, user_prompt, api_key, base_url, model, result, srt):
    mylogger.info("- 本地大模型/默认大模型翻译")
    mylogger.info("- 翻译内容：\n")
    client = OpenAI(api_key=api_key, base_url=base_url)
    segments = result['segments']
    segment_id = 0
    for segment in segments:
        text = segment['text']
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt + str(text)}
            ])
        answer = response.choices[0].message.content
        if srt == "原始语言为首":
            result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
        elif srt == "目标语言为首":
            result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
        else:
            result['segments'][segment_id]['text'] = answer
        segment_id += 1
        mylogger.info(answer)
    return result

"""
使用本地的大语言模型来进行翻译，接收srt
"""
def local_translate_srt(system_prompt, user_prompt, api_key, base_url, model, srt_content, srt):
    mylogger.info("- 本地大模型翻译")
    mylogger.info("- 翻译内容：\n")
    client = OpenAI(api_key=api_key, base_url=base_url)
    segment_id = 0
    for segment in srt_content:
        text = segment['text']
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt + str(text)}
            ])
        answer = response.choices[0].message.content
        if srt == "原始语言为首":
            srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
        elif srt == "目标语言为首":
            srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
        else:
            srt_content[segment_id]['text'] = answer
        segment_id += 1
        mylogger.info(answer)
    return srt_content

"""
将毫秒表示的时间转换为SRT字幕的时间格式
"""
def milliseconds_to_srt_time_format(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

"""
格式化为SRT字幕的形式，默认格式
"""
def generate_srt_from_result(result):
    segments = result['segments']
    srt_content = ''
    segment_id = 1
    for segment in segments:
        start_time = int(segment['start'] * 1000)
        end_time = int(segment['end'] * 1000)
        text = segment['text']

        srt_content += f"{segment_id}\n"
        srt_content += f"{milliseconds_to_srt_time_format(start_time)} --> {milliseconds_to_srt_time_format(end_time)}\n"
        srt_content += f"{text}\n\n"
        segment_id += 1
    return srt_content

"""
格式化为SRT字幕的形式，格式二
"""
def generate_srt_from_result_2(result, font, font_size, font_color):
    segments = result['segments']
    srt_content = ''
    segment_id = 1
    for segment in segments:
        start_time = int(segment['start'] * 1000)
        end_time = int(segment['end'] * 1000)
        text = segment['text']

        srt_content += f"{segment_id}\n"
        srt_content += f"{milliseconds_to_srt_time_format(start_time)} --> {milliseconds_to_srt_time_format(end_time)}\n"
        srt_content += f"<font color={font_color}><font face={font}><font size={font_size}> {text}\n\n"
        segment_id += 1
    return srt_content

"""
检测设备是否支持cuda
"""
def check_cuda_support():
    try:
        result = subprocess.run(["ffmpeg", "-hwaccels"], capture_output=True, text=True)
        return "cuda" in result.stdout
    except Exception as e:
        mylogger.info(f" 未检测到 CUDA 状态，本地合并为 CPU 模式，若要使用 GPU 请检查 CUDA 是否配置成功")
        return False

"""
字幕去除，这里的字幕去除也是基于ffmpeg
"""
def srt_mv(log, name, crf, quality, setting, path, font, font_size, font_color, subtitle_model):  # 视频合成字幕
    font_color = font_color.lstrip('#')  # 去掉 '#' 符号
    bb = font_color[4:6]
    gg = font_color[2:4]
    rr = font_color[0:2]
    font_color = f"&H{bb}{gg}{rr}&"
    cuda_supported = check_cuda_support()

    if subtitle_model == "硬字幕":
        if cuda_supported:
            command = f"""ffmpeg -loglevel {log} -hwaccel cuda -i {name} -lavfi "subtitles=output.srt:force_style='FontName={font},FontSize={font_size},PrimaryColour={font_color},Outline=1,Shadow=0,BackColour=&H9C9C9C&,Bold=-1,Alignment=2'" -preset {quality} -c:v {setting} -crf {crf} -y -c:a copy output.mp4"""
        else:
            command = f"""ffmpeg -loglevel {log} -i {name} -lavfi "subtitles=output.srt:force_style='FontName={font},FontSize={font_size},PrimaryColour={font_color},Outline=1,Shadow=0,BackColour=&H9C9C9C&,Bold=-1,Alignment=2'" -preset {quality} -c:v libx264 -crf {crf} -y -c:a copy output.mp4"""
    else:
        if cuda_supported:
            command = f"""ffmpeg -loglevel {log} -hwaccel cuda -i {name} -i output_with_style.srt -c:v {setting} -crf {crf} -y -c:a copy -c:s mov_text -preset {quality} output.mp4"""
        else:
            command = f"""ffmpeg -loglevel {log} -i {name} -i output_with_style.srt -c:v libx264 -crf {crf} -y -c:a copy -c:s mov_text -preset {quality} output.mp4"""

    subprocess.run(command, shell=True, cwd=path)

"""
SRT转换pandas.DataFrame对象方便展示
"""
def parse_srt_file(srt_content):
    lines = srt_content.strip().split('\n')
    subtitles = []
    current_subtitle = None

    for line in lines:
        line = line.strip()

        if line.isdigit():
            if current_subtitle is not None:
                subtitles.append(current_subtitle)
            current_subtitle = {'index': str(line)}
        elif '-->' in line:
            start_time, end_time = line.split('-->')
            current_subtitle['start'] = start_time.strip()
            current_subtitle['end'] = end_time.strip()
        elif line != '':
            if 'content' in current_subtitle:
                current_subtitle['content'] += '\n' + line
            else:
                current_subtitle['content'] = line

    if current_subtitle is not None:
        subtitles.append(current_subtitle)
    return pd.DataFrame(subtitles)

"""
将识别内容转化为srt
"""
def convert_to_srt(edited_data):
    subtitles = ''
    for index, row in edited_data.iterrows():
        start_time = row['start']
        end_time = row['end']
        content = row['content']
        subtitle = f"{index + 1}\n{start_time} --> {end_time}\n{content}\n\n"
        subtitles += subtitle
    return subtitles

"""
读取视频文件
"""
def show_video(path,name):
    with open(path + "/" + name, 'rb') as video_file:
        video_bytes = video_file.read()
    return video_bytes

"""
将SRT（SubRip字幕文件）格式的字幕内容转换为VTT
"""
def srt_to_vtt(srt_content):
    lines = srt_content.strip().split('\n')
    vtt_lines = ['WEBVTT\n\n']
    for i in range(0, len(lines), 4):
        index = lines[i].strip()
        time_range = lines[i + 1].strip().replace(',', '.')
        text = lines[i + 2].strip()
        vtt_lines.append(f'{index}\n{time_range}\n{text}\n\n')
    vtt_content = '\n'.join(vtt_lines)
    return vtt_content

"""
将SRT（SubRip字幕文件）格式的字幕内容转换为ASS
"""
def srt_to_ass(srt_content, fontname, size, color):
    lines = srt_content.strip().split('\n\n')
    ass_content = ('[Script Info]\nTitle: Converted from SRT\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,' + str(fontname) + ',' + str(size) + ',' + str(color) + ',&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0.00,1,1.00,0.00,2,10,10,10,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')
    for line in lines:
        parts = line.strip().split('\n')
        start, end = parts[1].split(' --> ')
        text = '\n'.join(parts[2:])
        ass_content += f'Dialogue: 0,{start},{end},Default,,0,0,0,,"{text}"\n'
    return ass_content

"""
将SRT（SubRip字幕文件）格式的字幕内容转换为STL
"""
def srt_to_stl(srt_content):
    lines = srt_content.strip().split('\n\n')
    stl_content = ''
    for i, line in enumerate(lines):
        parts = line.strip().split('\n')
        start, end = parts[1].split(' --> ')
        text = '\n'.join(parts[2:])
        text = text.replace('\n', ' ')
        stl_content += f'{i+1}\n{start} {end}\n{text}\n\n'
    return stl_content

"""
检测ffmpeg是否安装
"""
def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return False

"""
添加字体颜色
"""
def add_font_settings(srt_content, font_color, font_face, font_size):
    timestamp_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})")
    lines = srt_content.split("\n")
    result = []

    for line in lines:
        if line.isdigit():
            result.append(line)
        elif timestamp_pattern.match(line):
            result.append(line)
        elif line.strip() == "":
            result.append(line)
        else:
            formatted_line = f'<font color="{font_color}"><font face="{font_face}"><font size="{font_size}">{line}</font></font></font>'
            result.append(formatted_line)

    return "\n".join(result)

"""
解析字幕文件
"""
def read_srt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        srt = file.read().split('\n\n')
        timestamp_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})")
        subtitles = []

        for block in srt:
            lines = block.split('\n')
            if len(lines) >= 3:
                num = lines[0]
                times = lines[1]
                text = "\n".join(lines[2:])

                if timestamp_pattern.match(times):
                    subtitles.append({
                        'number': num,
                        'time': times,
                        'text': text
                    })

    return subtitles
