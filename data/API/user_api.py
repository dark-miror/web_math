import flask
from flask import jsonify, request

from .. import db_session
from ..db_table_files.users import User

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users': [item.to_dict() for item in users]
        }
    )


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict()
        }
    )


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['name', 'surname', 'email', 'password', 'avatar']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(User).get(request.json['id']):
        return jsonify({'error': 'ID already exists'})
    user = User()
    user.id = request.json['id']
    user.name = request.json['name']
    user.surname = request.json['surname']
    user.tasks = ""
    user.wrong_tasks = ""
    user.avatar = request.json['avatar']
    user.email = request.json['email']
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user', methods=['PUT'])
def edit_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['name', 'surname', 'email', 'password', 'avatar', 'tasks', 'wrong_tasks']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(request.json['id'])
    if not user:
        return jsonify({'error': 'ID does not exist'})
    user.id = request.json['id']
    user.name = request.json['name']
    user.surname = request.json['surname']
    user.tasks = request.json['tasks']
    user.wrong_tasks = request.json['wrong_tasks']
    user.avatar = request.json['avatar']
    user.email = request.json['email']
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})
