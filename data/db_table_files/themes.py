import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase


class Theme(SqlAlchemyBase):
    __tablename__ = 'themes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), nullable=True)
