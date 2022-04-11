from data.db_table_files.classes import Classes
from data.db_table_files.users import User
from data.db_table_files.themes import Theme
from data.db_table_files.tasks import Task
from data import db_session


def init():
    db_session.global_init("db/web_math.db")
    # new_class(7)
    # new_class(8)
    # new_class(9)
    # new_user("Anton", "Vityuk", "Кря!", "vityuka05@mail.ru", "1147labuda")
    # new_theme("Комбинаторка", 1)  # - пробное
    # new_task("a", 1, False)  # - пробное
    # new_theme("Линейное уравнение с одной переменной. Решение задач с помощью уравнений", 1)
    # new_task("Решение уравнений (1)", 1, 0)


def new_task(title, theme_id, task_test):
    task = Task()
    task.title = title
    task.theme_id = theme_id
    task.task_test = task_test
    db_sess = db_session.create_session()
    db_sess.add(task)
    db_sess.commit()


def new_theme(title, class_id):
    theme = Theme()
    theme.title = title
    theme.class_id = class_id
    db_sess = db_session.create_session()
    db_sess.add(theme)
    db_sess.commit()


def new_class(number):
    class_ = Classes()
    class_.number = number
    db_sess = db_session.create_session()
    db_sess.add(class_)
    db_sess.commit()


def new_user(name, surname, about, email, password, tasks=""):
    user = User()
    user.name = name
    user.surname = surname
    user.tasks = tasks
    user.about = about
    user.email = email
    user.set_password(password)
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
