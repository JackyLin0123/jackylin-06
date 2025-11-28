# 🧩 DataViz Platform — Login & Registration Module (Flask + MySQL + JWT)

一个基于 **Flask + MySQL + JWT** 的后端认证模块，采用面向对象（OOP）结构，可作为数据可视化平台的登录系统基础。
同时包含一个美观的前端测试页面（test_auth.html），可以直接在浏览器里测试接口，无需 Postman。
## ✨ Features

- 用户注册 / 登录
- 密码安全哈希（Werkzeug）
- JWT 登录态（Token 过期检测）
- Token 校验装饰器
- 完整 OOP 三层结构：Controller / Service / Repository / Model
- MySQL 数据库存储
- 跨域支持（flask-cors）
- 前端本地 Demo 页面可直接测试全部功能
## 📁 Project Structure
data_viz_platform/
│
├── app.py
├── config.py
├── db.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── test_auth.html
│
├── models/
│ ├── init.py
│ └── user.py
│
├── repositories/
│ ├── init.py
│ └── user_repository.py
│
└── services/
├── init.py
└── auth_service.py
## 🚀 Installation & Run Guide

本项目基于 **Flask + MySQL + Python 虚拟环境**。  
请按照以下步骤完成部署。

---

## 📌 1. 创建 Python 虚拟环境

建议使用项目独立虚拟环境，避免与系统依赖冲突。

```bash
python -m venv venv
激活虚拟环境（Windows）：

bash
复制代码
venv\Scripts\activate
激活成功后，命令行前会出现：

scss
复制代码
(venv)
📌 2. 安装项目依赖
虚拟环境启动后，运行：

bash
复制代码
pip install -r requirements.txt
依赖包含：

Flask

PyMySQL

Werkzeug

PyJWT

flask-cors

无需手动配置，自动安装。

📌 3. 配置 MySQL 数据库
首先登录 MySQL：

bash
复制代码
mysql -u root -p
3.1 创建数据库
sql
复制代码
CREATE DATABASE data_viz
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;
选择数据库：

sql
复制代码
USE data_viz;
3.2 创建 users 表
sql
复制代码
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
数据库已准备完毕 ✔

📌 4. 启动后端服务
确保你在项目根目录（包含 app.py 的目录）：

bash
复制代码
python app.py
成功后你将看到：

csharp
复制代码
 * Running on http://127.0.0.1:5000/
说明后端已经启动。

📌 5. 使用 test_auth.html 测试接口（无需 Postman）
项目提供一个前端测试页面：

复制代码
test_auth.html