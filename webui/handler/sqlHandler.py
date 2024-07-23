import time

import pymysql
from openai import OpenAI

def build_query_prompt(st,mode):

    # 在这里我们先初始化拿到SQLHelper再说
    if st.session_state.get("sqlAssistantHelper"):
        sqlAssistantHelper = st.session_state.sqlAssistantHelper
        sqlAssistantHelper.connect()
    else:
        sql_assistant_connect_config = st.session_state.sql_assistant_connect_config
        sqlAssistantHelper = SqlAssistantHelper(**sql_assistant_connect_config)
        sqlAssistantHelper.connect()
        st.session_state.sqlAssistantHelper = sqlAssistantHelper
    if mode == True:

        sqlContent = """"""
        tables = sqlAssistantHelper.get_all_tables()
        for table in tables:
            sqlContent+=f"table:{table}\n```sql \n {sqlAssistantHelper.get_create_table_statement(table)}\n ```\n"
        prompt = f"""你是一个SQL专家，接下来你将得到一个数据库的所有表的结构，你需要结合这些表的结构，来回答用户的问题
        下面是这些表的创建语句：
        {sqlContent}
        """
    else:
        # 获取当前选中的表
        current_select_table_name = st.session_state.current_select_table_name
        # 获取相关联的表
        sqlContent = """"""
        tables = sqlAssistantHelper.get_table_dependencies(current_select_table_name)
        for table in tables:
            sqlContent += f"table:{table}\n```sql \n {sqlAssistantHelper.get_create_table_statement(table)}\n ```\n"

        prompt = f"""你是一个SQL专家，接下来你将得到一个数据库的表和相关联的表，你需要结合这些表的结构，来回答用户的问题
        这个是用户当前选中的表：{current_select_table_name} 
        对应的结构是：
        ```sql
        {sqlAssistantHelper.get_create_table_statement(current_select_table_name)}
        ```
        相关联的表入下:
        {sqlContent}
        """
    sqlAssistantHelper.close_connection()
    # print("prompt:",prompt)
    return prompt

def sql_chat_assistant(st,config):

    # 查看当前的模式是什么模式
    # 为True表示当前模式为全量模式
    # 为False表示当前模式为部分模式
    sql_assistant_query_model = st.session_state.get("sql_assistant_query_model",False)
    if sql_assistant_query_model == True:
        start_tips = "当前模式为全量模式，将读取整个数据库的表结构回复问题👀，此部分对模型上下文要求较高！"
    else:
        start_tips = "当前模式为部分模式，将读取部分表结构回复问题👀，此部分对模型上下文要求较低！"
    sql_chat_assistant_messages = st.container(height=450)
    if "sql_chat_assistant_messages" not in st.session_state:
        st.session_state["sql_chat_assistant_messages"] = [
            {"role": "assistant", "content": start_tips}]
    else:
        st.session_state.sql_chat_assistant_messages[0] = {"role": "assistant", "content": start_tips}

    for msg in st.session_state.sql_chat_assistant_messages:
        sql_chat_assistant_messages.chat_message(msg["role"]).write(msg["content"])

    default_key = config["DEFAULT"]["default_key"]
    default_base = config["DEFAULT"]["default_base"]
    default_model = config["DEFAULT"]["default_model"]
    default_temperature = config["DEFAULT"]["default_temperature"]

    if (default_base != None and default_model != ""):
        placeholder = "有什么我可以帮你的么？😀"
    else:
        placeholder = "有什么我可以帮你的么？😀(请先设置默认大模型KEY)"
    if prompt := st.chat_input(placeholder=placeholder):
        client = OpenAI(api_key=default_key,
                        base_url=default_base,
                        )
        st.session_state.sql_chat_assistant_messages.append({"role": "user", "content": prompt})
        sql_chat_assistant_messages.chat_message("user").write(prompt)
        response = client.chat.completions.create(
            model=default_model,
            temperature=default_temperature,
            messages=[
                {"role": "system",
                 "content": build_query_prompt(st,sql_assistant_query_model)},
                {"role": "user", "content": prompt}
            ])
        try:
            msg = response.choices[0].message.content
            st.session_state.sql_chat_assistant_messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            print(e)
            msg = "抱歉，出现异常，请稍后再试~"
        with sql_chat_assistant_messages.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ''
            for item in msg:
                full_response += item
                time.sleep(0.01)
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)


class SqlAssistantHelper:
    def __init__(self, url,port, username, password, database):
        self.host = url
        self.port = port
        self.user = username
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(host=self.host,
                                              user=self.user,
                                              password=self.password,
                                              database=self.database,
                                              port=self.port,
                                              )
            return True
        except pymysql.MySQLError as e:
            print(f"数据库连接失败: {e}")
            return False

    def get_all_tables(self):
        """获取当前数据库的所有表名"""
        tables = []
        try:
            if self.connection is not None:
                with self.connection.cursor() as cursor:
                    cursor.execute("SHOW TABLES")
                    tables = [table[0] for table in cursor.fetchall()]

        except pymysql.MySQLError as e:
            print(f"获取表名失败: {e}")
        return tables

    def get_create_table_statement(self, table_name):
        """获取指定表的创建语句"""
        create_statement = None
        try:
            if self.connection is not None:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"SHOW CREATE TABLE {table_name}")
                    result = cursor.fetchone()
                    if result:
                        create_statement = result[1]  # "Create Table" 语句是第二个元素
        except pymysql.MySQLError as e:
            print(f"获取创建语句失败: {e}")
        return create_statement

    def get_table_dependencies(self, table_name):
        """获取指定表的依赖关系（外键）"""
        dependencies = []
        try:
            if self.connection is not None:
                with self.connection.cursor() as cursor:
                    # 获取该表作为外键引用的表
                    cursor.execute(f"""
                           SELECT TABLE_NAME 
                           FROM information_schema.KEY_COLUMN_USAGE 
                           WHERE 
                               CONSTRAINT_SCHEMA = '{self.database}' AND 
                               TABLE_NAME = '{table_name}' AND 
                               REFERENCED_TABLE_NAME IS NOT NULL;
                       """)
                    dependencies = [row[0] for row in cursor.fetchall()]

                    # 获取该表被其他表作为外键引用的情况
                    cursor.execute(f"""
                           SELECT REFERENCED_TABLE_NAME 
                           FROM information_schema.KEY_COLUMN_USAGE 
                           WHERE 
                               CONSTRAINT_SCHEMA = '{self.database}' AND 
                               REFERENCED_TABLE_NAME = '{table_name}';
                       """)
                    dependencies.extend([row[0] for row in cursor.fetchall()])
        except pymysql.MySQLError as e:
            print(f"获取依赖关系失败: {e}")
        return dependencies
    def close_connection(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")


# 使用示例
if __name__ == "__main__":
    # 配置数据库连接参数
    db_config = {
        'host': '127.0.0.1',
        'port':3306,
        'user': 'conven',
        'password': '123456789',
        'database': 'ConvenientMore'
    }

    # 创建 SqlHelper 实例
    sql_helper = SqlAssistantHelper(**db_config)

    # 连接数据库
    sql_helper.connect()

    # 获取所有表名
    all_tables = sql_helper.get_all_tables()
    print("所有表名:", all_tables)

    #获取指定表的创建语句
    table_name = 'la_system_auth_perm'  # 替换为你想要查看的表名
    create_statement = sql_helper.get_create_table_statement(table_name)
    if create_statement:
        print("表的创建语句:\n", create_statement)

    # 获取当前表的依赖外键
    table_name = 'la_system_auth_perm'  # 替换为你想要查看的表名
    dependencies = sql_helper.get_table_dependencies(table_name)
    print(f"表 {table_name} 的依赖关系:", dependencies)
    # 关闭数据库连接
    sql_helper.close_connection()