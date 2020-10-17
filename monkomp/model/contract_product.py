from monkomp.monkomp import db
from .contract import Contract
from .product import Product


contract_products = db.Table(
    'Contract_Product',
    db.Column('contract_id', db.Integer, db.ForeignKey('Contract.id'), primary_key=True),
    db.Column('factory_number', db.Integer, db.ForeignKey('Product.factory_number'), primary_key=True)
)
