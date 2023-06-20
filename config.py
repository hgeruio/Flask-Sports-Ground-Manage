# 配置文件

SECRET_KEY="fasgffewaf"

# 连数据库
localhost = "localhost"
username = "root"
password = "root"
database = "database"
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{localhost}/{database}?charset=utf8mb4"
