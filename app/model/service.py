from sqlalchemy.orm import validates
from .exceptions import ValidationError
from . import db


class Service(db.Model):
    __tablename__ = "Service"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128), nullable=False, unique=True)
    rate = db.Column(db.Integer, nullable=False)
    field_calls = db.relationship("FieldCall")

    def __repr__(self):
        return str(self.__dict__)

    @validates("rate")
    def validate_price(self, key, rate):
        if not rate.isdecimal():
            raise ValidationError("Rate has to be a decimal number.")
        return rate

    @property
    def serialize(self):
        return {"id": str(self.id), "name": self.name, "rate": str(self.rate)}

    @classmethod
    def from_dict(cls, serialized):
        for key, value in serialized.items():
            if not isinstance(value, str):
                raise ValidationError(
                    f"Field {key} has to be a string, not {type(value).__name__}."
                )
        try:
            return cls(**serialized)
        except ValueError as err:
            raise ValidationError(str(err))
