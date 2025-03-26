import flask
from flask import Flask, render_template, session, g
from sqlalchemy.sql.functions import current_user

import config
from exts import db, mail
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from models import UserModel
from flask_migrate import Migrate

app = Flask(__name__)
#绑定配置文件
app.config.from_object(config)
mail.init_app(app)
db.init_app(app)


migrate = Migrate(app, db)

#ORM模型映射成表的三步
#1. flask db init 这步只需要执行1次，
#2. flask db migrate 识别ORM模型的改变，生成迁移脚本
#3. flask db upgrade 运行迁移脚本， 同步到数据库中


app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


#Flask 中的 route() 装饰器用于将 URL 绑定到函数。
@app.route('/')
def index():
    return render_template('index.html')

#before_request/ before_first_request/ after_request
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    #app.run(host, port, debug, options)
    app.run(debug=True)  #使用debug方式运行


# 学习的知识点
# url
# 邮件发送
# ajax
# Jinja2模板
# cookie和session原理
# 搜索

# 后续学习
# 前端
#部署
# 《Flask全栈开发》
# 《Flask实战》 Flask+Vue前后端分享的论坛 WebSocket实战p