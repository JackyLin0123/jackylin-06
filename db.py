# db.py
import pymysql
from config import Config

class Database:
    """数据库连接封装类"""

    def __init__(self):
        self.host = Config.MYSQL_HOST
        self.port = Config.MYSQL_PORT
        self.user = Config.MYSQL_USER
        self.password = Config.MYSQL_PASSWORD
        self.db = Config.MYSQL_DB

    def get_connection(self):
        """获取一个新的数据库连接"""
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn

# 建一个全局 Database 实例，后面可以直接导入使用
db = Database()
