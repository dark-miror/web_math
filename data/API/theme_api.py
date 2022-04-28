import flask
from flask import jsonify, request

from .. import db_session
from ..db_table_files.themes import Theme

blueprint = flask.Blueprint(
    'tasks_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/theme')
def get_themes():
    db_sess = db_session.create_session()
    theme = db_sess.query(Theme).all()
    return jsonify(
        {
            'themes': [item.to_dict() for item in theme]
        }
    )


@blueprint.route('/api/theme/<int:theme_id>', methods=['GET'])
def get_one_theme(theme_id):
    db_sess = db_session.create_session()
    theme = db_sess.query(Theme).get(theme_id)
    if not theme:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'theme': theme.to_dict()
        }
    )


@blueprint.route('/api/theme', methods=['POST'])
def create_theme():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title', 'class_id']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(Theme).get(request.json['id']):
        return jsonify({'error': 'ID already exists'})
    theme = Theme(
        id=request.json['id'],
        title=request.json['title'],
        class_id=request.json['class_id']
    )
    db_sess.add(theme)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/theme/<int:theme_id>', methods=['DELETE'])
def delete_task(theme_id):
    db_sess = db_session.create_session()
    theme = db_sess.query(Theme).get(theme_id)
    if not theme:
        return jsonify({'error': 'Not found'})
    db_sess.delete(theme)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/theme', methods=['PUT'])
def edit_task():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title', 'class_id']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    theme = db_sess.query(Theme).get(request.json['id'])
    if not theme:
        return jsonify({'error': 'ID does not exist'})
    theme.id = request.json['id']
    theme.title = request.json['title']
    theme.class_id = request.json['class_id']
    db_sess.commit()
    return jsonify({'success': 'OK'})
