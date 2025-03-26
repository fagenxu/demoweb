from flask import Blueprint, render_template, request, g, redirect, url_for
from blueprints.forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from decorators import login_required
bp = Blueprint('qa', __name__, url_prefix='/')

# http://127.0.0.1:5000
@bp.route('/qa')
def qa():
    pass
@bp.route('/')
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('index.html', questions=questions)


@bp.route('/qa/detail/<qa_id>')

def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    if request.method == 'GET':
        return render_template("detail.html", question=question)



@bp.route('/qa/public', methods=['GET', 'POST'])
@login_required #引用登录限制，不登录时不可以访问此网页
def public_question():

    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            #关键SQL Model
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))





@bp.post('/answer/public')
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, author_id=g.user.id, question_id=question_id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))
@bp.route('/search')
def search():
    q = request.args.get('q')
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template('index.html', questions=questions)
