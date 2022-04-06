from flask import Flask
from data import db_session
from add_to_db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aboba_secret_key'


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


if __name__ == '__main__':
    main()