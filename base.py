"""
@FileName：base.py
@Author：Huterox
@Description：Go For It
@Time：2024/5/21 8:31
@Copyright：©2018-2024 awesome!
"""
import os
import shutil
import uuid
from datetime import datetime
import torch
from colorlog import ColoredFormatter

current_dir_root = os.path.dirname(os.path.abspath(__file__))

cache_dir_root = os.path.join(current_dir_root, "cache")
model_dir_root = os.path.join(current_dir_root, "model")
docs_dir_root = os.path.join(current_dir_root,"docs")

"""
********************************
*     对应组件的一些公共变量设置   *
********************************
"""


def create_signal_source(file_name, content):
    # 获取当前的年月日
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    target_folder_path = os.path.join(cache_dir_root, str(year), str(month).zfill(2), str(day).zfill(2),
                                      f"{uuid.uuid4()}")
    # 检查目标文件夹是否存在，如果不存在则创建
    os.makedirs(target_folder_path, exist_ok=True)
    file_name = f"{file_name}.mp4"
    # 构建完整的文件路径
    file_path = os.path.join(target_folder_path, file_name)
    # 创建文件
    with open(file_path, 'wb') as file:
        file.write(content)
    return file_path

def hex_to_rgb(hex_color):
    """
    将十六进制颜色字符串转换为RGB格式
    :param hex_color: 十六进制颜色字符串，例如 "#fdfbfb"
    :return: (R, G, B) 元组
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

"""
只根据名字，创建临时存储文件路径，不创建文件，交给真正生成视频的函去创建保存文件
"""
def create_signal_temp_source(file_type="mp4"):
    # 获取当前的年月日
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    target_folder_path = os.path.join(cache_dir_root, str(year), str(month).zfill(2), str(day).zfill(2),
                                      f"{uuid.uuid4()}")
    os.makedirs(target_folder_path, exist_ok=True)
    file_name = f"{uuid.uuid4()}."+file_type
    file_path = os.path.join(target_folder_path, file_name)

    return file_path

def create_signal_temp_source_floder():
    # 获取当前的年月日
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    target_folder_path = os.path.join(cache_dir_root, str(year), str(month).zfill(2), str(day).zfill(2),
                                      f"{uuid.uuid4()}")
    os.makedirs(target_folder_path, exist_ok=True)
    return target_folder_path

import logging
def setup_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger

mylogger = setup_logger()

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} has been deleted successfully.")
        else:
            print(f"File {file_path} does not exist.")
    except PermissionError:
        print(f"Permission denied: unable to delete {file_path}.")
    except FileNotFoundError:
        print(f"File not found: {file_path}.")
    except Exception as e:
        print(f"An error occurred while trying to delete the file: {e}")


def check_gpu():
    import torch
    cuda_available = torch.cuda.is_available()
    print(f"CUDA 是否可用: {cuda_available}")
    if cuda_available:
        num_gpus = torch.cuda.device_count()
        print(f"可用 GPU 数量: {num_gpus}")
        for i in range(num_gpus):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("没有可用的 GPU")


def delete_folder(folder_path):
    """
    删除指定的文件夹及其内容。

    参数:
    folder_path (str): 要删除的文件夹路径
    """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' has been deleted.")
    else:
        print(f"Folder '{folder_path}' does not exist.")


def is_cuda_available():
    """
    判断 CUDA 是否可用。

    返回:
    bool: 如果 CUDA 可用，返回 True；否则返回 False。
    """
    return torch.cuda.is_available()