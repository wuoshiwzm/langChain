from typing import List

from langchain.agents import create_agent
from langchain_core.tools import BaseTool

from agent.llm import llm_openai
from agent.tools.test_to_sql_tools import ListTableTool, TableSchemaTool, SQLQueryCheckTool, SQLQueryTool
from agent.utils.db_utils import MySqlDatabaseMgr


def get_tools() -> List[BaseTool]:
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

    sql_tools = [
        ListTableTool(db_manager=manager),
        TableSchemaTool(db_manager=manager),
        SQLQueryCheckTool(db_manager=manager),
        SQLQueryTool(db_manager=manager)
    ]
    return sql_tools


agent = create_agent(
    model=llm_openai,
    tools=get_tools(),
    system_prompt="""
        你是一个高效且智能的 Text-to-SQL 助手，目标是以最少但充分的工具调用，将用户问题转化为正确的 {sqltype} 查询。
        
        你的策略如下：
        - 利用上下文和常识推理用户可能使用的表。仅在表名不明确时，才调用 `ListTableTool`。
        - 仅对真正需要的表调用 `TableSchemaTool` 获取结构信息，避免冗余请求。
        - 基于真实 schema 编写精准 SQL，并**始终**通过 `SQLQueryCheckTool` 验证其合法性——此步骤不可省略。
        - 验证通过后，立即调用 `SQLQueryTool` 执行并返回结果。
        
        优化目标：
        - 在保证正确的前提下，尽量减少工具调用次数。
        - 复用已获取的信息（例如：若已知某表结构，无需重复查询）。
        - 能识别常见模式（如“上个月销售额” → 自动映射到日期字段和聚合函数）。
        
        约束条件：
        - 禁止执行未经验证的 SQL。
        - 绝对不要对数据库执行任何数据操作语言（DML）语句（如 INSERT, UPDATE, DELETE, DROP 等）
        - 禁止虚构表名或字段名。
        - 当不确定时，宁可多调一次工具，也不做错误假设。
        - 除非用户明确指定要获取的具体示例数据，否则始终将查询结果限制为最多{top_k}条
        
        最终输出应简洁明了。效率很重要，但绝不能牺牲正确性。
        。。。
    """.format(
        sqltype='MySQL',
        top_k=10
    )
)

# for step in agent.stream_run({'message': [{'role':'user','content':'请查询数据库中t_usermodel表中的id和name列，并返回前5条数据'}]}):
for step in agent.stream(
        input={'messages': [{'role': 'user', 'content': '数据库中有多少部门，每个部门有哪些员工?'}]},
        stream_mode='values'
):
    step['messages'][-1].pretty_print()
