import random
from mailbox import Message
from flask import request, jsonify, redirect, url_for, session

from flask import Blueprint, render_template
from pyexpat.errors import messages
from flask_mail import Message
import string

from werkzeug.security import generate_password_hash, check_password_hash

from blueprints.forms import RegisterFrom, LoginFrom

from exts import mail, db
from models import EmailCaptchaModel, UserModel

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginFrom(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在，请先注册！")
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                #cookie, 通过session保存到cookie中
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("密码错误@")
                return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))



@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        #验证用户提交的数据是否对应且正确
        #表单验证：flask-wtf: wtforms
        form = RegisterFrom(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
            #return redirect("login")
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))
            #return redirect("register")


@bp.route('/mail/test')
def mail_test():
    message = Message(subject="test", recipients=['fagen_xu@ks.gemteks.com'], body='中华人民共和国')
    mail.send(message)
    return 'ok'

@bp.route('/captcha/email')
def get_email_captcha():
    email = request.args.get('email')
    #4/6: 随机产生数字、字母、数组和字母的组合
    source = string.digits*4
    captcha = random.sample(source, 4)
    captcha = ''.join(captcha)
    message = Message(subject="注册验证码", recipients=[email], body=f'您的验证码是：{captcha}')
    mail.send(message)
    #用数据库表的方式存储
    email_captcha = EmailCaptchaModel(email = email, captcha = captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code": 200, "message": "", "data":None})

@bp.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

