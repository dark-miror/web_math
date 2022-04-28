import flask
from flask import jsonify, request

from .. import db_session
from ..db_table_files.tasks import Task

blueprint = flask.Blueprint(
    'tasks_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/task')
def get_tasks():
    db_sess = db_session.create_session()
    task = db_sess.query(Task).all()
    return jsonify(
        {
            'tasks': [item.to_dict() for item in task]
        }
    )


@blueprint.route('/api/task/<int:task_id>', methods=['GET'])
def get_one_task(task_id):
    db_sess = db_session.create_session()
    task = db_sess.query(Task).get(task_id)
    if not task:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'task': task.to_dict()
        }
    )


@blueprint.route('/api/task', methods=['POST'])
def create_task():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title', 'theme_id', 'task_test']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(Task).get(request.json['id']):
        return jsonify({'error': 'ID already exists'})
    task = Task(
        id=request.json['id'],
        title=request.json['title'],
        theme_id=request.json['theme_id'],
        task_test=request.json['task_test']
    )
    db_sess.add(task)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db_sess = db_session.create_session()
    task = db_sess.query(Task).get(task_id)
    if not task:
        return jsonify({'error': 'Not found'})
    db_sess.delete(task)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/task', methods=['PUT'])
def edit_task():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title', 'theme_id', 'task_test']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    task = db_sess.query(Task).get(request.json['id'])
    if not task:
        return jsonify({'error': 'ID does not exist'})
    task.id = request.json['id']
    task.title = request.json['title']
    task.theme_id = request.json['theme_id']
    task.task_test = request.json['task_test']
    db_sess.commit()
    return jsonify({'success': 'OK'})
