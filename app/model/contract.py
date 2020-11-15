from . import db
from flask import url_for
from datetime import datetime
from .exceptions import ValidationError
from sqlalchemy.orm import validates


class Contract(db.Model):
    __tablename__ = "Contract"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_number = db.Column(db.String(26), unique=True, nullable=False)
    signed_on = db.Column(db.DateTime, nullable=False)
    expires_on = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("Customer.id"), nullable=False)

    def __repr__(self):
        return str(self.__dict__)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "account_number": self.account_number,
            "signed_on": self.signed_on,
            "expires_on": self.expires_on,
            "customer": url_for("api.get_customer", id=self.customer_id),
        }

    @classmethod
    def from_dict(cls, serialized):
        try:
            return cls(
                account_number=serialized.get("account_number", None),
                expires_on=datetime.fromisoformat(serialized.get("expires_on", None)),
                signed_on=datetime.fromisoformat(serialized.get("signed_on", None)),
                customer_id=serialized.get("customer_id", None),
            )
        except ValueError as err:
            raise ValidationError(str(err))
