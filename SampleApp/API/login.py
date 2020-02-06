import json

from flask_login import login_user, login_required, logout_user
from itsdangerous import TimestampSigner, BadSignature, URLSafeSerializer, SignatureExpired

from SampleApp.DataManagement.db import User
from SampleApp import db, login_manager
from flask import (
    Blueprint, request, Response, session
)

from SampleApp.DataManagement.serialization import UserSchema

bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()

    if user is None:
        return Response(
            response=json.dumps({'message': 'user does not exists'}),
            status=401,
            mimetype='application/json'
        )
    elif user.check_password(password):
        login_user(user)

        return Response(
            response=json.dumps({'message': 'authentication successful'}),
            status=201,
            mimetype='application/json'
        )
    else:
        return Response(
            response=json.dumps({'message': 'authentication failed'}),
            status=401,
            mimetype='application/json'
        )


@bp.route('/register', methods=['POST'])
def register():
    username = request.json['username']

    user = User.query.filter_by(username=username).first()
    if user is not None:
        return Response(
            response=json.dumps({'message': f'username: {username} already exists'}),
            status=409,
            mimetype='application/json'
        )

    request.json['password'] = User.generate_password(request.json['password'])
    new_user = UserSchema().load(request.json)
    db.session.add(new_user)
    db.session.commit()

    return {'username': new_user.username}


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return Response(
            response=json.dumps({'message': 'logout successful'}),
            status=200,
            mimetype='application/json'
        )
    except Exception:
        return Response(
            response=json.dumps({'message': 'logout went wrong'}),
            status=404,
            mimetype='application/json'
        )


@login_manager.user_loader
def load_user(token):

    serializer = URLSafeSerializer('secret-key')
    serialized_token = serializer.loads(token)

    signer = TimestampSigner('secret-key')
    try:
        username = signer.unsign(serialized_token, max_age=1000)
    except SignatureExpired:
        session['failed_authentication_cause'] = 'token expired'
        return None
    except BadSignature:
        session['failed_authentication_cause'] = 'unauthorized token'
        return None

    user = User.query.filter_by(username=username.decode('utf-8')).first()
    return user


@login_manager.unauthorized_handler
def unauthorized():
    message = f'failed to authorize: {session["failed_authentication_cause"]}'
    return Response(
            response=json.dumps({'message': message}),
            status=401,
            mimetype='application/json'
        )


