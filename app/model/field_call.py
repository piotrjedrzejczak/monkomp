from .engineer import Engineer
from .service import Service
from . import db


class FieldCall(db.Model):
    __tablename__ = "FieldCall"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comments = db.Column(db.UnicodeText(1000))
    invoiced = db.Column(db.Boolean)
    receipt_amount = db.Column(db.Numeric(8, 2))
    settled = db.Column(db.Boolean)
    date = db.Column(db.DateTime)
    payment_type = db.Column(db.Unicode(32))
    engineer_id = db.Column(db.Integer, db.ForeignKey("Engineer.id"))
    service_id = db.Column(db.Integer, db.ForeignKey("Service.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("Customer.id"))
