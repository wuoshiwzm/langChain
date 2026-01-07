from typing import Any, Optional, List

from langchain_core.tools import BaseTool
from pydantic import create_model, Field

from agent.utils.db_utils import MySqlDatabaseMgr
from agent.utils.log_utils import logger


# 获取表名的工具
class ListTableTool(BaseTool):
    """列出数据库中所有的表及期描述信息"""
    name: str = 'sql_db_list_tables'
    description = '列出 MYSQL 数据库中的所有表名及其描述信息。当需要了解数据库中有哪些表以及表的用途时使用此工具'
    db_manager: MySqlDatabaseMgr

    def _run(self) -> str:
        try:
            table_infos = self.db_manager.get_tables_with_comments()
            result = f'数据库中共有{len(table_infos)}个表:\n\n'
            # 遍历 table infos
            for i, table_info in enumerate(table_infos):
                tbl_name = table_info['table_name']
                tbl_comment = table_info['table_comment']

                # 处理空描述
                description_display = tbl_comment if tbl_comment and not tbl_comment.isspace() else '(暂无描述)'

                result += f'{i + 1}.表名:{tbl_name}\n'
                result += f'  描述:{description_display}\n'
            return result
        except Exception as e:
            logger.exception(e)
            return f"ListTableTool Error: {e}"

    async def _arun(self) -> str:
        return self._run()

# 获取表结构的工具
class TableSchemaTool(BaseTool):
    """获取指定表的结构信息"""

    name = 'sql_db_schema'
    description = ('获取 MYSQL 数据库中指定表的结构信息,包括列定义，主键，外键等。'
                   '当需要了解某个表的字段名、数据类型、主键等详细结构时使用此工具。'
                   '输入应为逗号分隔的表名列表，或留空表示获取所有表的结构信息。')
    db_manager: MySqlDatabaseMgr

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Pydantic 把“任意数据”（如 JSON、字典、环境变量等）安全地转换成“结构化、类型正确的 Python 对象”，并在出错时给出清晰的错误信息
        self.args_schema = create_model(
            'TableSchemaToolArgs',
            table_names=(Optional[str],
                         Field(..., description='逗号分隔的表名列表，例如：t_usermodel, t_rolemodel')))

    def _run(self, table_names: Optional[str] = None) -> str:
        try:
            tbl_names = [name.strip() for name in table_names.split(',')] if table_names else None
            table_schema = self.db_manager.get_table_schema(tbl_names)
            return table_schema if table_schema else '未找到相关表结构信息'
        except Exception as e:
            logger.exception(e)
            return f"ListTableTool Error: {e}"

    async def _arun(self, table_names: Optional[str] = None) -> str:
        return self._run(table_names)

# 检查SQL的工具
class SQLQueryCheckTool(BaseTool):
    name = 'sql_db_query_checker'
    description = ('检查给定的 SQL 查询语句是否符合 MYSQL 语法规范，并提供修改建议。'
                   '当需要验证 SQL 查询的正确性或优化查询语句时使用此工具。')
    db_manager: MySqlDatabaseMgr

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args_schema = create_model('SQLQueryCheckToolArgs', query=(str, Field(..., description='要检查的SQL')))
    def _run(self, query: str) -> str:
        try:
            res = self.db_manager.validate_query(query)
            return res
        except Exception as e:
            logger.exception(e)
            return f"Query Execute Error: {e}"

    async def _arun(self, query: str) -> str:
        return self._run(query)

# 执行SQL的工具
class SQLQueryTool(BaseTool):
    name = 'sql_db_query'
    description = ('在 MYSQL 数据库中执行给定的 SQL 查询语句。'
                   '当需要从数据库获取数据、更新记录或执行其他数据库操作时使用此工具。')
    db_manager: MySqlDatabaseMgr

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args_schema = create_model('SQLQueryToolArgs', query=(str, Field(..., description='要执行的SQL')))

    def _run(self, query: str)->str:
        try:
            res = self.db_manager.execute_query(query)
            return res
        except Exception as e:
            logger.exception(e)
            return f"Query Execute Error: {e}"

    async def _arun(self, query: str) -> str:
        return self._run(query)

####### 测试
if __name__ == '__main__':
    # mysql8
    DB_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'username': 'root',
        'password': '12345',
        'database': 'test_db',
    }
    conn_str = (f"mysql+pymysql://{DB_CONFIG['username']}:{DB_CONFIG['DB_CONFIG']}@{DB_CONFIG['host']}:"
                f"{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    manager = MySqlDatabaseMgr(conn_str)

    # 测试工具1
    list_table_tool = ListTableTool(db_manager=manager)
    print(list_table_tool.invoke({}))

    # 测试工具2
    table_schema_tool = TableSchemaTool(db_manager=manager)
    print(table_schema_tool.invoke({}))
    print(table_schema_tool.invoke({'table_names':['t_usermodel', 't_rolemodel']}))

    # 测试工具3
    sql_check_tool = SQLQueryCheckTool(db_manager=manager)
    print(sql_check_tool.invoke({'query':'select * from t_usermodel'}))
    print(sql_check_tool.invoke({'query':'selectt * from t_usermodel'}))            # 错误的SQL，关键字 selectt 拼写错误
    print(sql_check_tool.invoke({'query':'select * from t_usermodel111'}))          # 错误的SQL，表名不存在
    print(sql_check_tool.invoke({'query':'select count() from t_usermodel111'}))    # 错误的SQL
    print(sql_check_tool.invoke({'query':'delete * from t_usermodel111'}))          # 错误的SQL，不能使用 delete 关键词，表名不存在

    # 测试工具4
    sql_execute_tool = SQLQueryTool(db_manager=manager)
    print(sql_execute_tool.invoke({'query':'select * from t_usermodel'}))



