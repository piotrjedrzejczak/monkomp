from flask import Flask
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    from .model import db
    from .model.customer import Customer
    from .model.contract import Contract
    from .model.contract_product import contract_products
    from .model.engineer import Engineer
    from .model.field_call import FieldCall
    from .model.product import Product
    from .model.service import Service
    db.init_app(app)
    db.create_all(app=app)

    from .api import api
    app.register_blueprint(api)

    return app
