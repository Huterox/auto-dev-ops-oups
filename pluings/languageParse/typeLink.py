"""
@FileName：typeLink.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/21 18:08
@Copyright：©2018-2024 awesome!
"""
from pluings.languageParse.typeParse import get_code_parse_adpate, BaseCodeAdapter


"""
构建适配器相关联的map
"""
def build_link_map(current_file_map):
    res = {}
    for file_name, fileItem in current_file_map.items():
        adapter_parse = get_code_parse_adpate(fileItem)
        res[file_name] = adapter_parse
    return res

"""
根据当前选定的代码文件，找到相互关联的文件
（这里是拿到适配器就好了，适配器里面有解析器，解析器里面有fileItem）
"""
def get_link_file(current:BaseCodeAdapter, link_map:dict[str,BaseCodeAdapter]):
    res = []
    current_import = current.get_import_str().split(",")
    for file_name, adapter in link_map.items():
        for import_str in current_import:
            adapter_de = adapter.get_defined_str()
            if import_str in adapter_de:
                res.append(adapter.parse.fileItem)
    return res
