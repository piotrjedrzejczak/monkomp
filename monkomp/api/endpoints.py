from flask import request
from flask.json import jsonify
from sqlalchemy.exc import IntegrityError
from monkomp.model.product import Product
from monkomp.model.customer import Customer
from monkomp.api.errors import bad_request, integrity_error_parser
from monkomp.monkomp import db
from monkomp.api import api



@api.route('/customers/')
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
            message = integrity_error_parser(error)
            return bad_request(message)



@api.route('/products/')
def all_products():
    collection = Customer.query.all()
    return jsonify([customer.serialize for customer in collection]), 200


@api.route("/products/<int:id>")
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.serialize), 200


@api.route("/products/new")
def new_product():
    payload = request.get_json(silent=True)
    if payload is None:
        return bad_request('Unable to convert the data to JSON format.')
    if not isinstance(payload, dict):
        return bad_request('Request data has to be a valid JSON object.')

