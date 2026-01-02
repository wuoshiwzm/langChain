from sqlalchemy import create_engine, inspect
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

    def get_tables(self):
        try:
            # 数据库映射对象
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            print(f'Sql error: {e}')
            logger.exception(e)
            raise ValueError(f'Err to get tables {str(e)}')

if __name__ == '__main__':
    # mysql8
    DB_CONFIG={
        'host': 'localhost',
        'port': 3306,
        'username': 'root',
        'password': '12345',
        'database': 'test_db',
    }
    conn_str = (f'mysql+pymysql://{DB_CONFIG["username"]}:{DB_CONFIG["DB_CONFIG"]}@{DB_CONFIG["host"]}:'
                f'{DB_CONFIG["port"]}/{DB_CONFIG["database"]}')
    manager = MySqlDatabaseMgr(DB_CONFIG)