import flask
from flask import jsonify, request

from .. import db_session
from ..db_table_files.classes import Classes

blueprint = flask.Blueprint(
    'classes_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/classes')
def get_classes():
    db_sess = db_session.create_session()
    classes = db_sess.query(Classes).all()
    return jsonify(
        {
            'classes': [item.to_dict() for item in classes]
        }
    )


@blueprint.route('/api/classes/<int:class_id>', methods=['GET'])
def get_one_class(class_id):
    db_sess = db_session.create_session()
    class_ = db_sess.query(Classes).get(class_id)
    if not class_:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'class': class_.to_dict()
        }
    )


@blueprint.route('/api/classes', methods=['POST'])
def create_class():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['number']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(Classes).get(request.json['id']) or db_sess.query(Classes).filter(
            Classes.number == request.json['number']):
        return jsonify({'error': 'ID already exists'})
    class_ = Classes(
        id=request.json['id'],
        number=request.json['number']
    )
    db_sess.add(class_)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/classes/<int:class_id>', methods=['DELETE'])
def delete_class(class_id):
    db_sess = db_session.create_session()
    class_ = db_sess.query(Classes).get(class_id)
    if not class_:
        return jsonify({'error': 'Not found'})
    db_sess.delete(class_)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/classes', methods=['PUT'])
def edit_class():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['number']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    class_ = db_sess.query(Classes).get(request.json['id'])
    if not class_:
        return jsonify({'error': 'ID does not exist'})
    class_.id = request.json['id']
    class_.number = request.json['number']
    db_sess.commit()
    return jsonify({'success': 'OK'})
