from sqlalchemy.orm import validates
from re import match
from .exceptions import ValidationError
from .contract import Contract
from .field_call import FieldCall
from . import db


class Customer(db.Model):

    __tablename__ = "Customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.Unicode(128), nullable=False)
    lastname = db.Column(db.Unicode(128), nullable=False)
    company_name = db.Column(db.Unicode(256), unique=True, nullable=False)
    city = db.Column(db.Unicode(128), nullable=False)
    street = db.Column(db.Unicode(128), nullable=False)
    email = db.Column(db.Unicode(128), unique=True, nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    nip = db.Column(db.String(10), unique=True, nullable=False)
    telephone = db.Column(db.String(11), unique=True)
    comments = db.Column(db.UnicodeText(1000))
    contracts = db.relationship("Contract")
    field_calls = db.relationship("FieldCall")

    def __repr__(self):
        return str(self.__dict__)

    @property
    def serialize(self):
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "company_name": self.company_name,
            "city": self.city,
            "street": self.street,
            "email": self.email,
            "postal_code": self.postal_code,
            "nip": self.nip,
            "telephone": self.telephone,
            "comments": self.comments,
        }

    @classmethod
    def from_dict(cls, serialized):
        for key, value in serialized.items():
            if not isinstance(value, str):
                raise ValidationError(
                    f"Field [{key}] has to be a string, not [{type(value).__name__}]."
                )
        try:
            return cls(**serialized)
        except TypeError as err:
            raise ValidationError(str(err))

    @validates("nip")
    def validate_nip(self, key, nip):
        if len(nip) != 10:
            raise ValidationError(
                f"Valid NIP Number has exactly ten digits, the one you passed has [{len(nip)}]."
            )
        if not nip.isdigit():
            raise ValidationError("Valid NIP Number only consists of digits.")
        checksum = sum(int(x) * y for x, y in zip(nip[:9], [6, 5, 7, 2, 3, 4, 5, 6, 7]))
        if checksum % 11 != int(nip[-1]):
            raise ValidationError(
                "Modulo checksum failed. You provided Invalid NIP Number."
            )
        return nip

    @validates("telephone")
    def validate_telephone(self, key, number):
        if not number.isdigit():
            raise ValidationError("Valid telephone number only consists of digits.")
        if len(number) != 9:
            raise ValidationError(
                f"Valid telephone number has exactly nine digits, the one you passed has [{len(number)}]."
            )
        return number

    @validates("postal_code")
    def validate_postal_code(self, key, code):
        if match(r"\d{2}-\d{3}", code) is None:
            raise ValidationError(
                "Provided postal code does not comply with the valid format [XX-XXX] where X stands for a digit."
            )
        return code
