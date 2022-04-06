from data.classes import Classes
from data.users import User
from data import db_session


def new_class(class_):
    Class = Classes()
    Class.class_ = class_
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
