from flask_login import login_user
from itsdangerous import Signer

from SampleApp.DataManagement.db import User
from flask import (
    Blueprint, request, Response
)


bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route('/', methods=['POST'])
def add_employee():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()

    if user.check_password(password):
        login_user(user)
        signer = Signer('secret-key')
        token = signer.sign(username)

        return Response(
            response={'message': 'authentication successful',
                      'token': token},
            status=201,
            mimetype='application/json'
        )

    return Response(
        response={'message': 'authentication failed'},
        status=401,
        mimetype='application/json'
    )

