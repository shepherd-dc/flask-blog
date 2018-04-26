from flask import Flask, render_template, request, redirect, url_for, flash, session
import config
from exts import db
from models import User, Question, Answer

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by(db.desc(Question.create_time)).all()
    }
    return render_template('index.html', **context)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            session['username'] = username
            session.permanent = True
            flash('登录成功！')
            return redirect(url_for('index'))
        else:
            return '用户名或密码错误！'

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        user = User.query.filter(User.email == email).first()
        
        if user:
            return '该用户已被注册！'
        elif email=='' or username=='' or password=='' or repassword=='':
            return '输入内容不能为空！'
        else:
            if password != repassword:
                return '两次输入的密码不一致！'
            else:
                user = User(email=email, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                flash('注册成功，请登录！')
                return redirect(url_for('login'))

@app.route('/question/', methods=['GET', 'POST'])
def question():
    is_login = session.get('username')
    if is_login:
        if request.method == 'GET':
            return render_template('question.html')
        else:
            title = request.form.get('title')
            content = request.form.get('content')
            if title == '' or content == '':
                return '输入内容不能为空！'
            else:
                author = User.query.filter(User.username == is_login).first()
                question = Question(title=title, content=content)
                question.author = author
                db.session.add(question)
                db.session.commit()
                flash('发布成功！')
                return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/detail/<question_id>/')
def detail(question_id):
    question_detail = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question_detail=question_detail)

@app.route('/answer/', methods=['POST'])
def answer():
    is_login = session.get('username')
    if is_login:
        content = request.form.get('content')
        question_id = request.form.get('question_id')
        # print(content,question_id)  
        answer = Answer(content=content)

        author = User.query.filter(User.username == is_login).first()
        answer.author = author

        question = Question.query.filter(Question.id == question_id).first()
        answer.question = question

        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('detail', question_id=question_id))
    else:
        return redirect(url_for('login'))

@app.context_processor
def login_username():
    login_username = session.get('username')
    if login_username:
        user = User.query.filter(User.username == login_username).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run()