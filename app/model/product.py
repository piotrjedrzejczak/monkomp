from sqlalchemy.orm import validates
from app.model.exceptions import ValidationError
from datetime import datetime
from . import db


class Product(db.Model):

    __tablename__ = "Product"
    factory_number = db.Column(db.Unicode(128), primary_key=True)
    serial_number = db.Column(db.Unicode(128), unique=True)
    name = db.Column(db.Unicode(128), nullable=False)
    last_service = db.Column(db.DateTime)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return str(self.__dict__)

    @validates("price")
    def validate_price(self, key, price):
        if not price.isdecimal():
            raise ValidationError("Price has to be a decimal number.")
        return price

    @property
    def serialize(self):
        return {
            "factory_number": self.factory_number,
            "serial_number": self.serial_number,
            "name": self.name,
            "last_service": str(self.last_service),
            "price": str(self.price),
        }

    @classmethod
    def from_dict(cls, serialized):
        for key, value in serialized.items():
            if not isinstance(value, str):
                raise ValidationError(
                    f"Field {key} has to be a string, not {type(value).__name__}."
                )
        try:
            return cls(
                factory_number=serialized.get("factory_number"),
                serial_number=serialized.get("serial_number"),
                name=serialized.get("name"),
                price=serialized.get("price"),
                last_service=datetime.fromisoformat(serialized.get("last_service")),
            )
        except ValueError as err:
            raise ValidationError(str(err))
