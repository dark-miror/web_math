from data.db_table_files.classes import Classes
from data.db_table_files.users import User
from data.db_table_files.themes import Theme
from data.db_table_files.tasks import Task
from data import db_session
from os import path


def check_file(file):
    return path.exists(file)


def new_task(name, class_id, theme_id, title, text, img=""):
    task = Task()
    task.name = name
    task.class_id = class_id
    task.theme_id = theme_id
    task.title = title
    task.text = text
    task.img = img
    if img != "" and not check_file(img):
        print(f"ERORR - файла {img} нет.")
        return
    db_sess = db_session.create_session()
    db_sess.add(task)
    db_sess.commit()


def new_theme(name, class_id):
    theme = Theme()
    theme.theme = name
    theme.class_id = class_id
    db_sess = db_session.create_session()
    db_sess.add(theme)
    db_sess.commit()


def new_class(number):
    Class = Classes()
    Class.number = number
    db_sess = db_session.create_session()
    db_sess.add(Class)
    db_sess.commit()


def new_user(name, surname, class_id, tasks, about, email, password):
    user = User()
    user.name = name
    user.surname = surname
    user.class_id = class_id
    user.tasks = tasks
    user.about = about
    user.email = email
    user.set_password(password)

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()