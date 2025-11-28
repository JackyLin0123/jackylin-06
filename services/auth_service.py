# services/auth_service.py

import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from repositories.user_repository import UserRepository

class AuthService:
    """认证业务逻辑：注册、登录、token 处理"""

    def __init__(self):
        self.user_repo = UserRepository()
        self.jwt_secret = Config.JWT_SECRET_KEY

    # ---------- 注册 ----------
    def register(self, username, email, password):
        # 基本校验
        if not username or not email or not password:
            raise ValueError("username, email and password are required")

        # 检查是否已存在
        existing = self.user_repo.get_by_username_or_email(username, email)
        if existing:
            raise ValueError("username or email already exists")

        # 生成密码哈希
        pwd_hash = generate_password_hash(password)

        # 创建用户
        user = self.user_repo.create_user(username, email, pwd_hash)

        # 注册成功后直接签发一个 token
        token = self._create_token(user)
        return user, token

    # ---------- 登录 ----------
    def login(self, email, password):
        if not email or not password:
            raise ValueError("email and password are required")

        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("invalid email or password")

        if not check_password_hash(user.password_hash, password):
            raise ValueError("invalid email or password")

        # 更新最近登录时间
        self.user_repo.update_last_login(user.id)

        token = self._create_token(user)
        return user, token

    # ---------- Token ----------
    def _create_token(self, user: "User"):
        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token

    def parse_token(self, token: str):
        """解析 token，返回 payload，如果无效则抛异常"""
        payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
        return payload
