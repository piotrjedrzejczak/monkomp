from api.exceptions import ValidationError
from api import api
from flask import jsonify


def bad_request(message):
    response = jsonify({'error': 'Bad Request', 'message': message})
    response.status_code = 400
    return response

@api.errorhandler(ValidationError)
def validation_error(error):
    return bad_request(error.args[0])
