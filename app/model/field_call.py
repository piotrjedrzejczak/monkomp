from .engineer import Engineer
from .service import Service
from flask import url_for
from sqlalchemy.orm import validates
from .exceptions import ValidationError
from datetime import datetime
from . import db


class FieldCall(db.Model):
    __tablename__ = "FieldCall"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comments = db.Column(db.UnicodeText(1000))
    invoiced = db.Column(db.Boolean, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    settled = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    payment_type = db.Column(db.Unicode(32), nullable=False)
    engineer_id = db.Column(db.Integer, db.ForeignKey("Engineer.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("Service.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("Customer.id"), nullable=False)

    def __repr__(self):
        return str(self.__dict__)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "comments": self.comments,
            "invoiced": self.invoiced,
            "total": self.total,
            "settled": self.settled,
            "date": self.date,
            "payment_type": self.payment_type,
            "engineer": url_for("api.get_engineer", id=self.engineer_id),
            "service": url_for("api.get_service", id=self.service_id),
            "customer": url_for("api.get_customer", id=self.customer_id),
        }

    @classmethod
    def from_dict(cls, serialized):
        try:
            return cls(
                comments=serialized.get("comments"),
                invoiced=serialized.get("invoiced"),
                total=serialized.get("total"),
                settled=serialized.get("settled"),
                date=datetime.fromisoformat(serialized.get("date")),
                payment_type=serialized.get("payment_type"),
                engineer_id=serialized.get("engineer_id"),
                service_id=serialized.get("service_id"),
                customer_id=serialized.get("customer_id"),
            )
        except ValueError as err:
            raise ValidationError(str(err))

    @validates("total")
    def validate_total(self, key, total):
        if not total.isdecimal():
            raise ValidationError("Receipt amount has to be a decimal number.")
        return total
