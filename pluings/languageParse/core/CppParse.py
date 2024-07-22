import re

class CppCodeParse:
    def __init__(self, fileItem):
        self.code = fileItem.content
        self.fileItem = fileItem
        self.includes = []
        self.defined_functions = []
        self.defined_classes = []

    def parse_includes(self):
        include_pattern = r'^\s*#include\s+["<](.+?)[">]'
        self.includes = re.findall(include_pattern, self.code, re.MULTILINE)

    def parse_definitions(self):
        # 匹配函数定义
        function_pattern = r'\b(\w+\s*[\*&]?)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)'
        # 匹配类定义
        class_pattern = r'\bclass\s+(\w+)'
        # 匹配类中的成员函数声明
        member_function_pattern = r'\b(\w+)\s+([a-zA-Z_]\w*)\s*\('
        self.defined_functions = re.findall(function_pattern, self.code)
        self.defined_classes = re.findall(class_pattern, self.code)
        # 将成员函数声明添加到函数列表中
        self.defined_functions.extend(re.findall(member_function_pattern, self.code))

    def get_includes(self):
        return self.includes

    def get_defined_functions(self):
        # 只返回函数名
        return [func[1] for func in self.defined_functions]

    def get_defined_classes(self):
        return self.defined_classes

    def __str__(self):
        return (f"Includes: {self.get_includes()}\n"
                f"Defined Functions: {self.get_defined_functions()}\n"
                f"Defined Classes: {self.get_defined_classes()}")

if __name__ == '__main__':

    cpp_code = """
    #include <iostream>
    #include <vector>
    
    class MyClass {
    public:
        void myMethod();
        void myOtherMethod() const;
    };
    
    void myFunction(int arg) {
        std::cout << "Hello, World!" << std::endl;
    }
    
    MyClass::myMethod() {
        // ...
    }
    """

    # 创建CppCodeParse对象
    # cpp_parser = CppCodeParse(cpp_code)
    # cpp_parser.parse_includes()
    # cpp_parser.parse_definitions()
    #
    # # 打印解析结果
    # print(cpp_parser)