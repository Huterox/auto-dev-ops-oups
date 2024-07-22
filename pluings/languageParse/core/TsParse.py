import re

class TsCodeParse:
    def __init__(self, fileItem):
        self.code = fileItem.content
        self.simple_imports = []
        self.from_imports = []
        self.defined_classes = []
        self.defined_functions = []
        self.fileItem = fileItem

    def parse_imports(self):
        simple_import_pattern = r'^\s*import\s+(\w+)\s+from\s+["\'](.+?)["\'];'
        from_import_pattern = r'^\s*import\s+{([^}]*)}\s+from\s+["\'](.+?)["\'];'
        self.simple_imports = re.findall(simple_import_pattern, self.code, re.MULTILINE)
        self.from_imports = re.findall(from_import_pattern, self.code, re.MULTILINE)

    def parse_definitions(self):
        class_pattern = r'^\s*class\s+(\w+)'
        function_pattern = r'^\s*function\s+(\w+)\s*\(([^)]*)\)\s*{'
        self.defined_classes = re.findall(class_pattern, self.code, re.MULTILINE)
        self.defined_functions = re.findall(function_pattern, self.code, re.MULTILINE)

    def get_simple_imports(self):
        return self.simple_imports

    def get_from_imports(self):
        # 返回模块名和类或函数的列表
        return [(match[1].strip(), match[0].split(',')) for match in self.from_imports]

    def get_defined_classes(self):
        return self.defined_classes

    def get_defined_functions(self):
        return [(func[0].strip(), func[1].split(',')) for func in self.defined_functions]

    def __str__(self):
        return (f"Simple Imports: {self.get_simple_imports()}\n"
                f"From Imports: {self.get_from_imports()}\n"
                f"Defined Classes: {self.get_defined_classes()}\n"
                f"Defined Functions: {self.get_defined_functions()}")

if __name__ == '__main__':

    ts_code = """
    import React from 'react';
    import { Component, PropTypes as PT } from 'prop-types';
    import * as Utils from 'utils';
    
    class MyClass {
        myMethod() {
            console.log('Hello, World!');
        }
    }
    
    function myFunction(param1, param2) {
        console.log('Function');
    }
    
    const arrowFunction = (param1, param2) => {
        console.log('Arrow Function');
    };
    """

    # 创建TsCodeParse对象
    # ts_parser = TsCodeParse(ts_code)
    # ts_parser.parse_imports()
    # ts_parser.parse_definitions()
    #
    # # 打印解析结果
    # print(ts_parser)