from flask_httpauth import HTTPBasicAuth
from flask import g, url_for, jsonify, request
from app.models import User
from app.api import bp
from app.api.errors import bad_request
from app import db


auth = HTTPBasicAuth()

@bp.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        bad_request('Missing arguments')
    if User.query.filter_by(username=username).first() is not None:
        bad_request('User already exists')
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201, {'Location': url_for('api.get_user', id=user.id, _external=True)}


@bp.route('/users/<int:id>', methods=['GET'])
@auth.login_required
def get_user(id):
    user = User.query.get(id)
    if not user:
        bad_request('User does not exist')
    return jsonify({'username': user.username})

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True
