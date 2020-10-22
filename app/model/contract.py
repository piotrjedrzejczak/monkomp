from . import db


class Contract(db.Model):
    __tablename__ = 'Contract'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_number = db.Column(db.String(26))
    signed_on = db.Column(db.DateTime)
    expires_on = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.id'), nullable=False)
