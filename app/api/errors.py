from ..model.exceptions import ValidationError
from . import api
from flask import jsonify


def bad_request(message):
    response = jsonify({'error': 'Bad Request', 'message': message})
    response.status_code = 400
    return response

@api.errorhandler(ValidationError)
def validation_error(error):
    return bad_request(error.args[0])

@api.errorhandler(404)
def resource_not_found(e):
    response = jsonify({'error': 'resource not found'})
    response.status_code = 404
    return response

def integrity_error_parser(error):
    constraint, _, tablefield = repr(error.orig.args[0]).partition(':')
    table, _, field = tablefield.replace("'", "").partition('.')
    if constraint.startswith("'UNIQUE"):
        return f'{table.lower().strip()} with this {field} already exists.'
    if constraint.startswith("'NOT NULL"):
        return f'{field} of {table.lower().strip()} cannot be empty.'
    return repr(error.orig)
