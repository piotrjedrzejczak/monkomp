from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    company_name = db.Column(db.Unicode(256))
    city = db.Column(db.Unicode(128))
    street = db.Column(db.Unicode(128))
    email = db.Column(db.Unicode(128))
    postal_code = db.Column(db.String(6))
    nip = db.Column(db.String(10))
    telephone = db.Column(db.String(11))
    comments = db.Column(db.UnicodeText(1000))
    contracts = db.relationship('Contract')
    field_calls = db.relationship('FieldCall')
    
class Product(db.Model):
    __tablename__ = 'Product'
    factory_number = db.Column(db.Unicode(128), primary_key=True)
    serial_number = db.Column(db.Unicode(128))
    name = db.Column(db.Unicode(128))
    last_service = db.Column(db.DateTime)
    price = db.Column(db.Numeric(8,2))

class FieldCall(db.Model):
    __tablename__ = 'FieldCall'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comments = db.Column(db.UnicodeText(1000))
    invoiced = db.Column(db.Boolean)
    receipt_amount = db.Column(db.Numeric(8,2))
    settled = db.Column(db.Boolean)
    date = db.Column(db.DateTime)
    payment_type = db.Column(db.Unicode(32))
    engineer_id = db.Column(db.Integer, db.ForeignKey('Engineer.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('Service.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.id'))

class Service(db.Model):
    __tablename__ = 'Service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))
    rate = db.Column(db.Numeric(6,2))
    field_calls = db.relationship('FieldCall')

class Contract(db.Model):
    __tablename__ = 'Contract'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_number = db.Column(db.String(26))
    signed_on = db.Column(db.DateTime)
    expires_on = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.id'), nullable=False)
    products = db.relationship('Product')

class Engineer(db.Model):
    __tablename__ = 'Engineer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    field_calls = db.relationship('FieldCall')

contract_products = db.Table(
    'Contract_Product',
    db.Column('contract_id', db.Integer, db.ForeignKey('Contract.id'), primary_key=True),
    db.Column('factory_number', db.Integer, db.ForeignKey('Product.factory_number'), primary_key=True)
)