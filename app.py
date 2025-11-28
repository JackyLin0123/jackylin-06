# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import jwt

from config import Config
from services.auth_service import AuthService

app = Flask(__name__)
CORS(app)

auth_service = AuthService()
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

# ---------- 登录校验装饰器 ----------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid token"}), 401

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token,
                app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        # 把 payload 挂到 request 上方便后面用
        request.user = payload
        return f(*args, **kwargs)
    return wrapper

# ---------- 注册接口 ----------
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    try:
        user, token = auth_service.register(username, email, password)
        return jsonify({
            "message": "register success",
            "token": token,
            "user": user.to_dict()
        }), 201
    except ValueError as e:
        # 业务错误，用 400/409
        msg = str(e)
        status = 400
        if "exists" in msg:
            status = 409
        return jsonify({"message": msg}), status
    except Exception as e:
        # 未预料错误
        return jsonify({"message": "server error", "detail": str(e)}), 500

# ---------- 登录接口 ----------
@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    try:
        user, token = auth_service.login(email, password)
        return jsonify({
            "message": "login success",
            "token": token,
            "user": user.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 401
    except Exception as e:
        return jsonify({"message": "server error", "detail": str(e)}), 500

# ---------- 获取当前登录用户 ----------
@app.route("/api/auth/me", methods=["GET"])
@login_required
def get_me():
    return jsonify({
        "message": "ok",
        "user": {
            "id": request.user["user_id"],
            "username": request.user["username"]
        }
    }), 200

# ---------- 示例：受保护的图表接口 ----------
@app.route("/api/charts/overview", methods=["GET"])
@login_required
def charts_overview():
    # 这里就可以根据 request.user["user_id"] 查该用户的数据
    dummy_data = {
        "total_users": 120,
        "active_today": 35
    }
    return jsonify(dummy_data), 200

if __name__ == "__main__":
    app.run(debug=True)
