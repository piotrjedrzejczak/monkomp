from monkomp.monkomp import db

class Product(db.Model):
    __tablename__ = 'Product'
    factory_number = db.Column(db.Unicode(128), primary_key=True)
    serial_number = db.Column(db.Unicode(128))
    name = db.Column(db.Unicode(128))
    last_service = db.Column(db.DateTime)
    price = db.Column(db.Numeric(8,2))
