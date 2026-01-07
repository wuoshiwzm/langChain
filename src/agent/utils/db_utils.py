import json
from typing import Optional, List

from charset_normalizer.api import explain_handler
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

from agent.utils.log_utils import logger


class MySqlDatabaseMgr:
    """Mysql 数据库管理器，实现数据库连接与基本操作"""

    def __init__(self, connection_string: str):
        """
        初始化 MYSQL 数据库连接

        Args:
           connection_string: Mysql 连接字符串，格式为
                mysql+pymysql://user:password@host:port/database
        """
        self.engine = create_engine(connection_string, pool_size=5, pool_recycle=3600)

    def get_table_names(self) -> List[str]:
        try:
            # 数据库映射对象
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            print(f'Sql error: {e}')
            logger.exception(e)
            raise ValueError(f'Err to get tables {str(e)}')

    def get_tables_with_comments(self) -> List[dict]:
        """
        获取表名及描述信息
        :return:
        """
        try:
            query = text("""
                         SELECT TABLE_NAME, TABLE_COMMENT
                         FROM INFORMATION_SCHEMA.TABLES
                         WHERE TABLE_SCHEMA = DATABASE()
                           AND TABLE_TYPE = 'BASE TABLE'
                         ORDER BY TABLE_NAME
                         """)

            with self.engine.connect() as conn:
                result = conn.execute(query)
                table_info = [{'table_name': row[0], 'table_comment': row[1]} for row in result]
                return table_info

        except SQLAlchemyError as e:
            print(f'Sql error: {e}')
            logger.exception(e)
            raise ValueError(f'Err to get tables with comments {str(e)}')

    def get_table_schema(self, table_names: Optional[List[str]] = None) -> str:
        """
        获取指定表的模式信息（包含字段注释）
        :param table_names: 表名列表，如果为 None 则获取所有表
        :return:
        """
        try:
            inspector = inspect(self.engine)
            schema_info = []

            tables_to_process = table_names if table_names else self.get_table_names()
            for tables_name in tables_to_process:
                # 获取表结构信息
                columns = inspector.get_columns(tables_name)

                # get_pk_constraint 替代已经弃用的 get_primary_keys
                pk_constraint = inspector.get_pk_constraint(tables_name)
                primary_keys = pk_constraint.get('constrained_columns', []) if pk_constraint else []
                foreign_keys = inspector.get_foreign_keys(tables_name)
                indexes = inspector.get_indexes(tables_name)

                # 构建表模式描述
                table_schema = f'表名:{tables_name}\n'
                table_schema += '列信息:\n'

                for column in columns:
                    # 检查该列是否是主键列表中
                    pk_indicator = '(主键)' if column['name'] in primary_keys else ''
                    comment = column.get('comment', '无注释')
                    table_schema += f"  - {column['name']}: {str(column['type'])}{pk_indicator}[注释:{comment}]"

                if foreign_keys:
                    table_schema += '外键约束:\n'
                    for foreign in foreign_keys:
                        table_schema += f"    - {foreign['constrained_columns']} -> {foreign['referred_table']}.{foreign['referred_columns']}\n"

                if indexes:
                    table_schema += '索引信息:\n'
                    for index in indexes:
                        if not index['name'].startswith('sqlite_'):
                            table_schema += f"    - {index['column_names']} [{'唯一' if index['unique'] else '非唯一'}]\n"

                schema_info.append(table_schema)
            return '\n'.join(schema_info) if schema_info else '未找到匹配的表'
        except SQLAlchemyError as e:
            print(f'Sql error: {e}')
            logger.exception(e)
            raise ValueError(f'Err to get tables with schema {str(e)}')

    def execute_query(self, query: str) -> str:

        forbidden_keywords = ['insert', 'update', 'delete', 'drop', 'create', 'alter', 'grant', 'truncate']
        query_lower = query.lower().strip()

        # 检查是否以 SELECT 开头（允许子查询等复杂查询）
        if not query_lower.startswith('select', 'with') and any(
                keyword in query_lower for keyword in forbidden_keywords):
            raise ValueError('只允许 SELECT 查询')

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                columns = result.keys()
                # 限制返回行数 防止内存溢出
                rows = result.fetchmany(100)
                if not rows:
                    return '查询无结果'

                # 格式化输出
                result_data = []
                for row in rows:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        # 无法序列化的数据类型
                        try:
                            if row[i] is not None:
                                json.dumps(row[i])
                            row_dict[col] = row[i]
                        except (TypeError, OverflowError):
                            row_dict[col] = str(row[i])
                    result_data.append(row_dict)
                return json.dumps(result_data, ensure_ascii=False, indent=2)
        except SQLAlchemyError as e:
            logger.exception(e)
            raise ValueError(f'Err to execute sql {str(e)}')

    def validate_query(self, query: str) -> str:
        """
        使用 SQLAlchemy 验证SQL语法是否正确
        :param query:
        :return:
        """
        if not query or not query.strip():
            return '查询语句不能为空'
        query_lower = query.lower().strip()

        # 预执行（不实际执行）
        try:

            # 方法一：使用 sqlalchemy 的 compile 方法检查
            with self.engine.connect() as conn:
                parsed_query = text(query)
                compiled = parsed_query.compile(compile_kwargs={'literal_binds': True})
                return 'SQL seems right'

            # 方法二：使用 MySql 的 EXPLAIN 语句执行 （只支持 MySql）
            # with self.engine.connect() as conn:
            #     if self.engine.dialect == 'mysql':
            #         explain_query = test(f'EXPLAIN {query}')
            #     else: # POSTGRESQL, REDIS 等数据库的语法不同
            #         explain_query = text(f'SELECT 1 FROM ({query}) AS t LIMIT 0')
            #     conn.execute(explain_query)
            #     return 'SQL seems right( has pass EXPLAIN check)'

        except SQLAlchemyError as e:
            logger.exception(e)
            raise ValueError(f'Err to execute sql {str(e)}')


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
