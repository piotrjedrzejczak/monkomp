from flask import request
from flask.json import jsonify
from sqlalchemy.exc import IntegrityError

from model.customer import Customer
from api.errors import bad_request
from monkomp import db
from api import api


@api.route('/customers')
def all_customers():
    collection = Customer.query.all()
    return jsonify([customer.serialize for customer in collection]), 200


@api.route('/customers/<int:id>')
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.serialize), 200


@api.route("/customers/new", methods=['POST'])
def new_customer():
    payload = request.get_json(silent=True)
    if payload is None:
        return bad_request('Unable to convert the data to JSON format.')
    if not isinstance(payload, dict):
        return bad_request('Request data has to be a valid JSON object.')
    else:
        try:
            db.session.add(Customer.from_dict(payload))
            db.session.commit()
            return {"added": "1"}, 201
        except IntegrityError as error:
            db.session.rollback()
            message = repr(error.orig).partition('UNIQUE')
            if message[1]:
                field = message[2].partition('.')[2][:-2]
                return bad_request(f'Customer with this {field} already exists.')
            else:
                return bad_request(repr(error.orig))

