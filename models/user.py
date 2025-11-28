# models/user.py

class User:
    """用户实体类，对应 users 表的一行数据"""

    def __init__(self, id=None, username=None, email=None,
                 password_hash=None, created_at=None, last_login=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.last_login = last_login

    def to_dict(self):
        """返回给前端时用的字典（不包含密码）"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": str(self.created_at) if self.created_at else None,
            "last_login": str(self.last_login) if self.last_login else None
        }
