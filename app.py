from flask import Flask, render_template, request, redirect, url_for, flash, session
import config
from exts import db
from models import User

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

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
        else:
            if password != repassword:
                return '两次输入的密码不一致！'
            else:
                user = User(email=email, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                flash('注册成功，请登录！')
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