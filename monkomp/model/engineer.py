from monkomp.monkomp import db


class Engineer(db.Model):
    __tablename__ = 'Engineer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    field_calls = db.relationship('FieldCall')
    email = db.Column(db.Unicode(128))
