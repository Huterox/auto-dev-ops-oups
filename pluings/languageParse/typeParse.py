"""
@FileName：typeParse.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/21 17:42
@Copyright：©2018-2024 awesome!
"""
from pluings.languageParse.core.CParse import CCodeParse
from pluings.languageParse.core.CppParse import CppCodeParse
from pluings.languageParse.core.JavaParse import JavaCodeParse
from pluings.languageParse.core.JsParse import JsCodeParse
from pluings.languageParse.core.PythonParse import PyCodeParse
from pluings.languageParse.core.TsParse import TsCodeParse
from webui.handler.assistantHandler import FileItem

"""
根据当前存在的解析器构建对应的解析器，这些解析器是多例模式的
"""

CODE_PARSE_MAP = {
    "ts":TsCodeParse,
    "py":PyCodeParse,
    "js":JsCodeParse,
    "java":JavaCodeParse,
    "cpp":CppCodeParse,
    "c":CCodeParse
}


def get_code_parse(fileItem:FileItem):
    """
    根据文件类型获取对应的解析器
    :param fileItem:
    :return:
    """
    parseClass = CODE_PARSE_MAP.get(fileItem.type,None)
    if parseClass:
        parse = parseClass(fileItem)
        return parse
    else:
        return None

"""
接下来我们再定义几个适配器类，方便我们直接调用
"""
class BaseCodeAdapter:
    def __init__(self, parse):
        self.parse = parse

    def get_import_str(self):

        raise NotImplementedError("Subclasses should implement this method.")

    def get_defined_str(self):

        raise NotImplementedError("Subclasses should implement this method.")

class CCodeAdpateCode(BaseCodeAdapter):
    def __init__(self, parse: CCodeParse):
        super().__init__(parse)

    def add_str(self, res: str, parse_res):
        for im in parse_res:
            if isinstance(im, tuple):
                # 如果是元组，还要提取出元组里面的数组当中的值
                for m in im:
                    if isinstance(m, list):
                        for s in m:
                            res += f"{s},"
            else:
                res += f"{im},"
        return res
    # 查看当前的这个代码导入了哪些类，方法
    def get_import_str(self):
        self.parse.parse_includes()
        res = ''
        res = self.add_str(res, self.parse.get_includes())
        res = res[0:len(res) - 1]
        return res


    def get_defined_str(self):
        self.parse.parse_definitions()
        res = ''
        res = self.add_str(res, self.parse.get_defined_functions())
        res = res[0:len(res) - 1]
        return res

class CppCodeAdpateCode(BaseCodeAdapter):
    def __init__(self, parse: CppCodeParse):
        super().__init__(parse)

    def add_str(self, res: str, parse_res):
        for im in parse_res:
            if isinstance(im, tuple):
                # 如果是元组，还要提取出元组里面的数组当中的值
                for m in im:
                    if isinstance(m, list):
                        for s in m:
                            res += f"{s},"
            else:
                res += f"{im},"
        return res
    # 查看当前的这个代码导入了哪些类，方法
    def get_import_str(self):
        self.parse.parse_includes()
        res = ''
        res = self.add_str(res, self.parse.get_includes())
        res = res[0:len(res) - 1]
        return res


    def get_defined_str(self):
        self.parse.parse_definitions()
        res = ''
        res = self.add_str(res, self.parse.get_defined_classes())
        res += self.add_str(res, self.parse.get_defined_functions())
        res = res[0:len(res) - 1]
        return res


class JavaCodeAdpateCode(BaseCodeAdapter):
    def __init__(self, parse: JavaCodeParse):
        super().__init__(parse)

    def add_str(self, res: str, parse_res):
        for im in parse_res:
            if isinstance(im, tuple):
                # 如果是元组，还要提取出元组里面的数组当中的值
                for m in im:
                    if isinstance(m, list):
                        for s in m:
                            res += f"{s},"
            else:
                res += f"{im},"
        return res

    # 查看当前的这个代码导入了哪些类，方法
    def get_import_str(self):
        self.parse.parse_imports()
        res = ''
        res = self.add_str(res, self.parse.get_imports())
        res = res[0:len(res) - 1]
        return res


    def get_defined_str(self):
        self.parse.parse_definitions()
        res = ''
        res = self.add_str(res, self.parse.get_defined_classes())
        res += self.add_str(res, self.parse.get_defined_methods())
        res = res[0:len(res) - 1]
        return res

class JsCodeAdpateCode(BaseCodeAdapter):
    def __init__(self, parse: JsCodeParse):
        super().__init__(parse)

    # 查看当前的这个代码导入了哪些类，方法
    def get_import_str(self):
        self.parse.parse_imports()
        res = ''
        res = self.add_str(res, self.parse.get_simple_imports())
        res += self.add_str(res, self.parse.get_from_imports())
        res = res[0:len(res) - 1]
        return res


    def add_str(self,res:str,parse_res):
        for im in parse_res:
            if isinstance(im, tuple):
                # 如果是元组，还要提取出元组里面的数组当中的值
                for m in im:
                    if isinstance(m, list):
                        for s in m:
                            res += f"{s},"
            else:
                res += f"{im},"
        return res

    def get_defined_str(self):
        self.parse.parse_definitions()
        res = ''
        res = self.add_str(res,self.parse.get_defined_classes())
        res += self.add_str(res,self.parse.get_defined_functions())
        res = res[0:len(res) - 1]
        return res


class PyCodeAdpateCode(BaseCodeAdapter):
    def __init__(self, parse: PyCodeParse):
        super().__init__(parse)


    def add_str(self,res:str,parse_res):
        for im in parse_res:
            if isinstance(im,tuple):
                # 如果是元组，还要提取出元组里面的数组当中的值
                for m in im:
                    if isinstance(m,list):
                        for s in m:
                            if s != '__init__':
                                res += f"{s},"
            else:
                if im != '__init__':
                    res += f"{im},"
        return res

    # 查看当前的这个代码导入了哪些类，方法
    def get_import_str(self):
        self.parse.parse_imports()
        res = ''
        res = self.add_str(res, self.parse.get_simple_imports())
        res += self.add_str(res, self.parse.get_from_imports())
        res = res[0:len(res) - 1]
        return res



    def get_defined_str(self):
        self.parse.parse_definitions()
        res = ''
        res = self.add_str(res, self.parse.get_defined_classes())
        res += self.add_str(res, self.parse.get_defined_functions())
        res = res[0:len(res) - 1]
        return res


class TsCodeAdpateCode(BaseCodeAdapter):
    def __init__(self,parse:TsCodeParse):
        super().__init__(parse)

    def add_str(self,res:str,parse_res):
        for im in parse_res:
            if isinstance(im, tuple):
                # 如果是元组，还要提取出元组里面的数组当中的值
                for m in im:
                    if isinstance(m, list):
                        for s in m:
                            res += f"{s},"
            else:
                res += f"{im},"
        return res

    # 查看当前的这个代码导入了哪些类，方法
    def get_import_str(self):
        self.parse.parse_imports()
        res = ''
        res = self.add_str(res, self.parse.get_simple_imports())
        res += self.add_str(res, self.parse.get_from_imports())
        res = res[0:len(res) - 1]
        return res

    def get_defined_str(self):
        self.parse.parse_definitions()
        res = ''
        res = self.add_str(res, self.parse.get_defined_classes())
        res += self.add_str(res, self.parse.get_defined_functions())
        res = res[0:len(res)-1]
        return res


CODE_PARSE_ADPATE_MAP = {
    "ts":TsCodeAdpateCode,
    "py":PyCodeAdpateCode,
    "js":JsCodeAdpateCode,
    "java":JavaCodeAdpateCode,
    "cpp":CppCodeAdpateCode,
    "c":CCodeAdpateCode
}

def get_code_parse_adpate(fileItem:FileItem):
    """
    根据文件类型获取对应的解析器
    :param fileItem:
    :return:
    """
    parseClass = CODE_PARSE_MAP.get(fileItem.type,None)
    if parseClass:
        parse = parseClass(fileItem)
        adpateClass = CODE_PARSE_ADPATE_MAP.get(fileItem.type)
        adpate = adpateClass(parse)
        return adpate
    else:
        return None
