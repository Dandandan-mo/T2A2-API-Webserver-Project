from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, Length, And

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    street_number = db.Column(db.String, nullable=False)
    street_name = db.Column(db.String, nullable=False)
    suburb = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User')


class AddressSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['first_name', 'last_name', 'phone_number'])

    street_number = fields.String(required=True, validate=And(
        Regexp("^[0-9a-zA-Z.'#@%& -/]+$", error='Only numbers, letters, spaces and valid characters for address are allowed.'),
        Length(min=1, error='At least one character is required.')
    ))
    street_name = fields.String(required=True, validate=And(
        Regexp("^[0-9a-zA-Z.'#@%& -/]+$", error='Only numbers, letters, spaces and valid characters for address are allowed.'),
        Length(min=2, error='At least two characters are required.')
    ))
    suburb = fields.String(required=True, validate=And(
        Regexp("^[a-zA-Z.'#@%& -/]+$", error='Only letters, spaces and valid characters for address are allowed.'),
        Length(min=2, error='At least two characters are required.')
    ))
    postcode = fields.String(required=True, validate=And(
        Regexp('^[0-9a-zA-Z]+$', error='Only numbers and letters are allowed.'),
        Length(min=4, max=12, error='Valid postcode length is 4-12 characters.')
    ))
    class Meta:
        fields = ('id', 'street_number', 'street_name', 'suburb', 'postcode', 'user_id', 'user')
        ordered = True