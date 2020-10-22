from .exceptions import ValidationError
from . import api
from flask import jsonify


def bad_request(message):
    response = jsonify({'error': 'Bad Request', 'message': message})
    response.status_code = 400
    return response

@api.errorhandler(ValidationError)
def validation_error(error):
    return bad_request(error.args[0])

def integrity_error_parser(error):
    message = repr(error.orig)
    if message.find('UNIQUE') > 0:
        field = message.partition('.')[2][:-2]
        return f'Customer with this {field} already exists.'
    elif message.find('NOT NULL') > 0:
        field = message.partition('.')[2][:-2]
        return f'Field {field} cannot be empty.'
    else:
        return repr(error.orig)