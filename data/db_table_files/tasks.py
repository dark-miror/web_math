import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    theme_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("themes.id"), nullable=True)
    task_test = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)