import json

from flask_login import login_user
from itsdangerous import Signer, BadSignature

from SampleApp.DataManagement.db import User
from SampleApp import db, login_manager
from flask import (
    Blueprint, request, Response
)

from SampleApp.DataManagement.serialization import UserSchema

bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()

    if user.check_password(password):
        login_user(user)
        signer = Signer('secret-key')
        token = signer.sign(username)

        return Response(
            response=json.dumps({'message': 'authentication successful',
                                 'token': str(token)}),
            status=201,
            mimetype='application/json'
        )

    return Response(
        response=json.dumps({'message': 'authentication failed'}),
        status=401,
        mimetype='application/json'
    )


@bp.route('/register', methods=['POST'])
def register():
    print(request.json)
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


@login_manager.request_loader
def load_user_from_request(request):
    token = request.args.get('token')
    signer = Signer('secret-key')
    try:
        print(token)
        username = signer.unsign(token)
    except BadSignature:
        return None

    return  User.query.filter_by(username=username).first()
