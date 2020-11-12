from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from .exceptions import ValidationError
from . import db


class Engineer(db.Model):
    __tablename__ = "Engineer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.Unicode(128), nullable=False)
    lastname = db.Column(db.Unicode(128), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    field_calls = db.relationship("FieldCall")

    def __repr__(self):
        return str(self.__dict__)

    @property
    def serialize(self):
        return {
            "id": url_for("api.get_customer", id=self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
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
                firstname=serialized.get("firstname"),
                lastname=serialized.get("lastname"),
                email=serialized.get("email").lower(),
                password=serialized.get("password"),
            )
        except ValueError as err:
            raise ValidationError(str(err))

    @property
    def password(self):
        raise AttributeError(
            "password is not a readable attribute, use verify_password instead"
        )

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id}).decode("utf-8")

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None
        return Engineer.query.get(data["id"])
