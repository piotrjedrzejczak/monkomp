from flask import g
from flask_httpauth import HTTPBasicAuth
from . import api
from .errors import forbidden, unauthorized
from ..model.engineer import Engineer

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if not email_or_token:
        return False
    if not password:
        g.current_user = Engineer.verify_auth_token(email_or_token)
        return g.current_user is not None
    engineer = Engineer.query.filter_by(email=email_or_token.lower()).first()
    if not engineer:
        return False
    g.current_user = engineer
    return engineer.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized("invalid authentication credentials")


@api.before_request
@auth.login_required
def before_request():
    pass
