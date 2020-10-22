from . import db


class Service(db.Model):
    __tablename__ = 'Service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))
    rate = db.Column(db.Numeric(6,2))
    field_calls = db.relationship('FieldCall')
