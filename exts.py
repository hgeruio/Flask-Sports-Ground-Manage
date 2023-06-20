from flask_sqlalchemy import SQLAlchemy
# 存放扩展，防止循环引用

db = SQLAlchemy()  # 读取数据库信息，连接