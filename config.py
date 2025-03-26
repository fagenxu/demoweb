#设置cookie、session加密
SECRET_KEY = "SFWEsdfweffgsfwefwf"

# 创建数据库引擎（请修改连接字符串）
DATABASE_URL = "mysql+pymysql://root:Gemtek-kd@10.4.1.125/demoweb"
SQLALCHEMY_DATABASE_URI = DATABASE_URL

#邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USERNAME = '46404221@qq.com'
MAIL_PASSWORD = 'kxmnidmofvlvbjhd'
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = MAIL_USERNAME
