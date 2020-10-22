from flask.blueprints import Blueprint

api = Blueprint('api', __name__)

from . import errors, endpoints