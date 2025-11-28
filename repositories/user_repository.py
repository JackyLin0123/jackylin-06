# repositories/user_repository.py

from db import db
from models.user import User

class UserRepository:
    """用户数据访问层，所有对 users 表的操作都写在这里"""

    def create_user(self, username, email, password_hash):
        """插入新用户，返回 User 实例"""
        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (username, email, password_hash))
                conn.commit()
                user_id = cursor.lastrowid

                # 再查一次完整记录
                cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
                row = cursor.fetchone()
                return self._row_to_user(row)
        finally:
            conn.close()

    def get_by_email(self, email):
        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                row = cursor.fetchone()
                return self._row_to_user(row) if row else None
        finally:
            conn.close()

    def get_by_username_or_email(self, username, email):
        """注册时检查是否存在同名或同邮箱"""
        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE username=%s OR email=%s",
                    (username, email)
                )
                row = cursor.fetchone()
                return self._row_to_user(row) if row else None
        finally:
            conn.close()

    def update_last_login(self, user_id):
        conn = db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET last_login = NOW() WHERE id=%s",
                    (user_id,)
                )
                conn.commit()
        finally:
            conn.close()

    def _row_to_user(self, row):
        """把数据库查出的字典转成 User 对象"""
        return User(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            password_hash=row["password_hash"],
            created_at=row.get("created_at"),
            last_login=row.get("last_login")
        )
