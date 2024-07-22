import re

class JsCodeParse:
    def __init__(self, fileItem):
        self.code = fileItem.content
        self.fileItem = fileItem
        self.simple_imports = []
        self.from_imports = []
        self.defined_classes = []
        self.defined_functions = []

    def parse_imports(self):
        simple_import_pattern = r'^\s*import\s+([\w\s,{}*]+)from\s+["\'](\w+)["\'];'
        from_import_pattern = r'^\s*import\s+["\'](\w+)["\']\s+from\s+["\'](\w+)["\'];'
        self.simple_imports = re.findall(simple_import_pattern, self.code, re.MULTILINE)
        self.from_imports = re.findall(from_import_pattern, self.code, re.MULTILINE)

    def parse_definitions(self):
        class_pattern = r'^\s*class\s+(\w+)'
        function_pattern = r'^\s*function\s+(\w+)\s*\(([^)]*)\)\s*{'
        self.defined_classes = re.findall(class_pattern, self.code, re.MULTILINE)
        self.defined_functions = re.findall(function_pattern, self.code, re.MULTILINE)

    def get_simple_imports(self):
        return [(match[1], match[0].replace("*", "")) for match in self.simple_imports]

    def get_from_imports(self):
        return [(match[1], match[0]) for match in self.from_imports]

    def get_defined_classes(self):
        return self.defined_classes

    def get_defined_functions(self):
        return [(func[0], func[1].split(",")) for func in self.defined_functions]

    def __str__(self):
        return (f"Simple Imports: {self.get_simple_imports()}\n"
                f"From Imports: {self.get_from_imports()}\n"
                f"Defined Classes: {self.get_defined_classes()}\n"
                f"Defined Functions: {self.get_defined_functions()}")

if __name__ == '__main__':

    js_code = """
    import React from 'react';
    import { Component, PropTypes } from 'prop-types';
    import * as Utils from 'utils';
    
    class MyClass {
        myMethod() {
            console.log('Hello, World!');
        }
    }
    
    function myFunction() {
        console.log('Function');
    }
    
    const arrowFunction = () => {
        console.log('Arrow Function');
    };
    """

    # 创建JsCodeParse对象
    # js_parser = JsCodeParse(js_code)
    # js_parser.parse_imports()
    # js_parser.parse_definitions()
    #
    # # 打印解析结果
    # print(js_parser)