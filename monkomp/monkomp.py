from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from model.customer import Customer
    from model.contract import Contract
    from model.contract_product import contract_products
    from model.engineer import Engineer
    from model.field_call import FieldCall
    from model.product import Product
    from model.service import Service
    db.create_all(app=app)

    from api.endpoints import api
    app.register_blueprint(api)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)