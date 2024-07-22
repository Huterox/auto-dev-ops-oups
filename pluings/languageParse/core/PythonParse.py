import re

from webui.handler.assistantHandler import FileItem


class PyCodeParse:
    def __init__(self, fileItem):
        self.code = fileItem.content
        self.fileItem = fileItem
        self.simple_imports = []
        self.from_imports = []
        self.defined_classes = []
        self.defined_functions = []

    def parse_imports(self):
        simple_import_pattern = r'^\s*import\s+(\w+)'
        # from_import_pattern = r'^\s*from\s+(\w+)\s+import\s+([\w ,]+)'
        from_import_pattern = r'^\s*from\s+([\w\.]+)\s+import\s+(.*?)(?=\s*$|,|#)'
        self.simple_imports = re.findall(simple_import_pattern, self.code, re.MULTILINE)
        self.from_imports = re.findall(from_import_pattern, self.code, re.MULTILINE)

    def parse_definitions(self):
        class_pattern = r'^\s*class\s+(\w+):'
        function_pattern = r'^\s*def\s+(\w+)\s*\('
        self.defined_classes = re.findall(class_pattern, self.code, re.MULTILINE)
        self.defined_functions = re.findall(function_pattern, self.code, re.MULTILINE)

    def get_simple_imports(self):
        return self.simple_imports

    def get_from_imports(self):
        return [(module, items.split(',')) for module, items in self.from_imports]

    def get_defined_classes(self):
        return self.defined_classes

    def get_defined_functions(self):
        return self.defined_functions

    def __str__(self):
        return (f"Simple Imports: {self.get_simple_imports()}\n"
                f"From Imports: {self.get_from_imports()}\n"
                f"Defined Classes: {self.get_defined_classes()}\n"
                f"Defined Functions: {self.get_defined_functions()}")


if __name__ == "__main__":
    with open(r'F:\projects\MatchPro\AutoDevOps-oups\webui\CodingAssistant.py','r', encoding='utf-8') as f:
        python_code = f.read()
    fileItem = FileItem()
    fileItem.content = python_code
    import_parser = PyCodeParse(fileItem)
    import_parser.parse_imports()
    import_parser.parse_definitions()
    # 打印解析结果
    print(import_parser)