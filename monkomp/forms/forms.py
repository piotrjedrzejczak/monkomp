from monkomp.forms.validators import validate_nip, validate_telephone
from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField,
    IntegerField,
    RadioField,
    PasswordField,
    SelectMultipleField,
    ValidationError
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    NumberRange, Regexp
)


class CreateUserForm(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    company_name = StringField('company_name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    street = StringField('street', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email(message='Invalid Email')])
    postal_code = StringField('postal_code', validators=[DataRequired(), Regexp(r'[\d]{2}-[\d]{3}')])
    nip = StringField('nip', validators=[DataRequired(), validate_nip()])
    telephone = StringField('telephone', validators=[DataRequired(), validate_telephone])
    comments = StringField('comments', validators=[Optional()])

