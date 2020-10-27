from app.model.exceptions import ValidationError
from datetime import datetime
from . import db

class Product(db.Model):

    __tablename__ = 'Product'
    factory_number = db.Column(db.Unicode(128), primary_key=True)
    serial_number = db.Column(db.Unicode(128), unique=True)
    name = db.Column(db.Unicode(128), nullable=False)
    last_service = db.Column(db.DateTime)
    price = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return str(self.__dict__)

    @property
    def serialize(self):
        return {
            'factory_number': self.factory_number,
            'serial_number': self.serial_number,
            'name': self.name,
            'last_service': str(self.last_service),
            'price': str(self.price)
        }

    @classmethod
    def from_dict(cls, serialized):
        try:
            return cls(
                factory_number=serialized['factory_number'],
                serial_number=serialized['serial_number'],
                name=serialized['name'],
                price=serialized['price'],
                last_service=datetime.fromisoformat(serialized['last_service'])
            )
        except ValueError as err:
            raise ValidationError(str(err))