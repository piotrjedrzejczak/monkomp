from flask import request, g
from flask.json import jsonify
from sqlalchemy.exc import IntegrityError
from ..model import db
from ..model.product import Product
from ..model.customer import Customer
from ..model.service import Service
from ..model.field_call import FieldCall
from ..model.contract import Contract
from .errors import bad_request, integrity_error_parser
from . import api


@api.route("/token", methods=["POST"])
def get_token():
    return (
        jsonify(
            {
                "token": g.current_user.generate_auth_token(expiration=3600),
                "expiration": "3600",
            }
        ),
        200,
    )


@api.route("/engineers/<int:id>")
def get_engineer(id):
    raise NotImplementedError


@api.route("/engineers/update", methods=["PATCH"])
def update_engineer():
    raise NotImplementedError


@api.route("/customers/")
def all_customers():
    collection = Customer.query.all()
    return jsonify([customer.serialize for customer in collection]), 200


@api.route("/customers/<int:id>")
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.serialize), 200


@api.route("/customers/new", methods=["POST"])
def new_customer():
    payload = request.get_json(silent=True)
    if payload is None:
        return bad_request("Unable to convert the data to JSON format.")
    if not isinstance(payload, dict):
        return bad_request("Request data has to be a valid JSON object.")
    try:
        db.session.add(Customer.from_dict(payload))
        db.session.commit()
        return {"added": "1"}, 201
    except IntegrityError as error:
        db.session.rollback()
        message = integrity_error_parser(error)
        return bad_request(message)


@api.route("/products/")
def all_products():
    collection = Product.query.all()
    return jsonify([product.serialize for product in collection]), 200


@api.route("/products/<fac_num>")
def get_product(fac_num):
    product = Product.query.get_or_404(fac_num)
    return jsonify(product.serialize), 200


@api.route("/products/new", methods=["POST"])
def new_product():
    payload = request.get_json(silent=True)
    if payload is None:
        return bad_request("Unable to convert the data to JSON format.")
    if not isinstance(payload, dict):
        return bad_request("Request data has to be a valid JSON object.")
    try:
        db.session.add(Product.from_dict(payload))
        db.session.commit()
        return {"added": "1"}, 201
    except IntegrityError as error:
        db.session.rollback()
        message = integrity_error_parser(error)
        return bad_request(message)


@api.route("/services/")
def all_services():
    collection = Service.query.all()
    return jsonify([service.serialize for service in collection]), 200


@api.route("/services/<int:id>")
def get_service(id):
    service = Service.query.get_or_404(id)
    return jsonify(service.serialize), 200


@api.route("/services/new", methods=["POST"])
def new_service():
    payload = request.get_json(silent=True)
    if payload is None:
        return bad_request("Unable to convert the data to JSON format.")
    if not isinstance(payload, dict):
        return bad_request("Request data has to be a valid JSON object.")
    try:
        db.session.add(Service.from_dict(payload))
        db.session.commit()
        return {"added": "1"}, 201
    except IntegrityError as error:
        db.session.rollback()
        message = integrity_error_parser(error)
        return bad_request(message)


@api.route("/field-calls/")
def all_field_calls():
    collection = FieldCall.query.all()
    return jsonify([field_call.serialize for field_call in collection]), 200


@api.route("/field-calls/<int:id>")
def get_field_call(id):
    field_call = FieldCall.query.get_or_404(id)
    return jsonify(field_call.serialize), 200


@api.route("/field-calls/new", methods=["POST"])
def new_field_call():
    payload = request.get_json(silent=True)
    if payload is None:
        return bad_request("Unable to convert the data to JSON format.")
    if not isinstance(payload, dict):
        return bad_request("Request data has to be a valid JSON object.")
    try:
        db.session.add(FieldCall.from_dict(payload))
        db.session.commit()
        return {"added": "1"}, 201
    except IntegrityError as error:
        db.session.rollback()
        message = integrity_error_parser(error)
        return bad_request(message)


@api.route("/contracts/")
def all_contracts():
    collection = Contract.query.all()
    return jsonify([contract.serialize for contract in collection]), 200


@api.route("/contracts/<int:id>")
def get_contract(id):
    contract = Contract.query.get_or_404(id)
    return jsonify(contract.serialize), 200


@api.route("/contracts/new", methods=["POST"])
def new_contract():
    payload = request.get_json(silent=True)
    if payload is None:
        return bad_request("Unable to convert the data to JSON format.")
    if not isinstance(payload, dict):
        return bad_request("Request data has to be a valid JSON object.")
    try:
        db.session.add(Contract.from_dict(payload))
        db.session.commit()
        return {"added": "1"}, 201
    except IntegrityError as error:
        db.session.rollback()
        message = integrity_error_parser(error)
        return bad_request(message)
