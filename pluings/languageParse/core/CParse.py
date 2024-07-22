"""
@FileName：CParse.py
@Author：Huterox
@Description：Go For It
@Time：2024/7/21 16:58
@Copyright：©2018-2024 awesome!
"""
import re

class CCodeParse:
    def __init__(self, fileItem):
        self.fileItem = fileItem
        self.code = fileItem.content
        self.includes = []
        self.defined_functions = []

    def parse_includes(self):
        # 匹配 #include 语句
        include_pattern = r'^\s*#include\s+["<](.+?)[">]'
        self.includes = re.findall(include_pattern, self.code, re.MULTILINE)

    def parse_definitions(self):
        # 匹配函数定义
        # 匹配模式：返回类型 函数名 ( 参数列表 )
        function_pattern = r'\b(\w+)\s+(\w+)\s*\(([^)]*)\)'
        self.defined_functions = re.findall(function_pattern, self.code)

    def get_includes(self):
        return self.includes

    def get_defined_functions(self):
        # 返回函数名
        return [func[1] for func in self.defined_functions]

    def __str__(self):
        return (f"Includes: {self.get_includes()}\n"
                f"Defined Functions: {self.get_defined_functions()}")

if __name__ == '__main__':

    c_code = """
    #include <stdio.h>
    #include <stdlib.h>
    
    int add(int a, int b) {
        return a + b;
    }
    
    void sayHello() {
        printf("Hello, World!\n");
    }
    """

    # 创建CCodeParse对象
    # c_parser = CCodeParse(c_code)
    # c_parser.parse_includes()
    # c_parser.parse_definitions()
    #
    # # 打印解析结果
    # print(c_parser)
