from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.db_table_files.users import User
from data.db_table_files.classes import Classes
from data.db_table_files.themes import Theme
from data.db_table_files.tasks import Task
from add_to_db import *
from forms.login import LoginForm
from forms.register import RegisterForm


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'aboba_secret_key'


def clear_table(table):
    db_sess = db_session.create_session()
    db_sess.query(table).filter().delete()
    db_sess.commit()


def main():
    init()
    app.run(host='0.0.0.0', port=5000)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form,
                                   message="Такой пользователь уже есть")
        new_user(form.name.data, form.surname.data, form.about.data, form.email.data,
                 form.password.data)
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route("/")
def index():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        classes = db_sess.query(Classes).all()
        return render_template("index.html", classes=classes)
    return redirect('/login')


@app.route('/theme_choice/<int:id>')  # <int:id> – id класса
@login_required
def theme_choice(id):
    db_sess = db_session.create_session()
    themes = db_sess.query(Theme).filter(Theme.class_id == id).all()
    return render_template('theme.html', themes=themes)


@app.route('/theme_choice/type_work/<int:id>')  # <int:id> – id темы
@login_required
def type_work(id):
    db_sess = db_session.create_session()
    theme = db_sess.query(Theme).filter(Theme.id == id).first()
    return render_template('type_work.html', theme=theme)


@app.route('/theme_choice/type_work/theory/<int:id>')  # <int:id> – id темы
@login_required
def theory(id):
    return render_template(f"theory/{id}.html", theme_id=id)


@app.route('/theme_choice/type_work/tasks/<int:id>')  # <int:id> – id темы
@login_required
def task_choice(id):
    db_sess = db_session.create_session()
    tasks = db_sess.query(Task).filter(Task.theme_id == id).all()
    return render_template('tasks.html', tasks=tasks)


@app.route('/theme_choice/type_work/tasks/task/<int:id>')  # <int:id> – id задачи
@login_required
def task(id):
    db_sess = db_session.create_session()
    task = db_sess.query(Task).filter(Task.id == id).first()
    return render_template(f'tasks/{id}.html', task=task)


@app.route('/theme_choice/type_work/tasks/solves/<int:id>')  # <int:id> – id задачи
@login_required
def solve(id):
    db_sess = db_session.create_session()
    task = db_sess.query(Task).filter(Task.id == id).first()
    return render_template(f'solves/{id}.html', task=task)


if __name__ == '__main__':
    main()
