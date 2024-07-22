import re

class JavaCodeParse:
    def __init__(self, fileItem):
        self.code = fileItem.content
        self.fileItem = fileItem
        self.imports = []
        self.defined_classes = []
        self.method_names = []

    def parse_imports(self):
        import_pattern = r'^\s*import\s+([\w.]+);'
        self.imports = re.findall(import_pattern, self.code, re.MULTILINE)
        ims = []
        for im in self.imports:
            ims.append(im.split('.')[-1])
        self.imports = ims
    def parse_definitions(self):
        class_pattern = r'\bclass\s+(\w+)'
        method_pattern = r'\b(?:public|protected|private|static|synchronized)*\s+(\w+\s+)+(\w+)\s*\(([^)]*)\)'
        self.defined_classes = re.findall(class_pattern, self.code)
        self.method_names = re.findall(method_pattern, self.code)

    def get_imports(self):
        return self.imports

    def get_defined_classes(self):
        return self.defined_classes

    def get_defined_methods(self):
        # 只返回方法名
        return [method[1] for method in self.method_names]

    def __str__(self):
        return (f"Imports: {self.get_imports()}\n"
                f"Defined Classes: {self.get_defined_classes()}\n"
                f"Defined Methods: {self.get_defined_methods()}")

if __name__ == '__main__':

    java_code = """
    import java.util.List;
    import java.io.*;
    
    public class HelloWorld {
        private int number;
    
        public HelloWorld() {
        }
    
        public void sayHello(String name) {
            System.out.println("Hello, " + name);
        }
    }
    """

    # 创建JavaCodeParse对象
    # java_parser = JavaCodeParse(java_code)
    # java_parser.parse_imports()
    # java_parser.parse_definitions()
    #
    # # 打印解析结果
    # print(java_parser)