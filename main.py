from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
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


def init():
    db_session.global_init("db/web_math.db")
    # new_class(7)
    # new_class(8)
    # new_class(9)
    # new_user("Anton", "Vityuk", 3, "", "Кря!", "vityuka05@mail.ru", "1147labuda")
    # new_theme("Комбинаторка", 1)  # - пробное
    # new_task("a", 1, 1, "b", "c", 'static/tasks_img/a/a.jpeg')  # - пробное


def main():
    init()
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/")
def index():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        # jobs = db_sess.query(Jobs).all()
        return render_template("index.html")
    return redirect('/login')


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
        new_user(form.name.data, form.surname.data, form.class_num, "", form.about.data,
                 form.email.data, form.password.data)
        return redirect('/login')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    main()
