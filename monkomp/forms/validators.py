from functools import reduce
from wtforms import ValidationError
from re import match

def validate_nip(form, field):
    if len(field.data) != 10:
        raise ValidationError('Valid NIP number has exactly 11 digits')
    if not field.data.isdigit():
        raise ValidationError('Valid NIP number only consists of digits')
    acc = sum(int(x) * y for x, y in zip(field.data[:9], [6,5,7,2,3,4,5,6,7]))
    if acc % 11 != int(field.data[-1]):
        raise ValidationError('Invalid NIP number')

def validate_telephone(form, field):
    if not field.data.isdigit():
        raise ValidationError('Valid telephone number only consists of digits')
    if len(field.data) != 9:
        raise ValidationError('Valid telephone number has exactly 9 digits')