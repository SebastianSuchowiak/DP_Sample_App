from flask_login import LoginManager
from itsdangerous import Signer, BadSignature
from SampleApp.DataManagement.db import User
from SampleApp import login_manager


@login_manager.request_loader
def load_user_from_request(request):
    token = request.args.get('session_token')
    signer = Signer('secret-key')
    try:
        username = signer.unsign(token)
    except BadSignature:
        return None

    return  User.query.filter_by(username=username).first()
