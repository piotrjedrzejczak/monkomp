from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from monkomp.model.customer import Customer
    from monkomp.model.contract import Contract
    from monkomp.model.contract_product import contract_products
    from monkomp.model.engineer import Engineer
    from monkomp.model.field_call import FieldCall
    from monkomp.model.product import Product
    from monkomp.model.service import Service
    db.create_all(app=app)

    from monkomp.api.endpoints import api
    app.register_blueprint(api)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)