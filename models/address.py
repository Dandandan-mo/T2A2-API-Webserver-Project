from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    street_number = db.Column(db.String, nullable=False)
    street_name = db.Column(db.String, nullable=False)
    suburb = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User', back_populates='addresses')
    # shipments = db.relationship('Shipment', back_populates='address')

class AddressSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['first_name', 'last_name', 'phone_number'])

    street_number = fields.String(required=True, validate=Regexp('^[0-9a-zA-Z]+$', error='Only numbers and letters are allowed.'))
    street_name = fields.String(required=True, validate=Regexp('^[0-9a-zA-Z]+$', error='Only numbers and letters are allowed.'))
    suburb = fields.String(required=True, validate=Regexp('^[a-zA-Z]+$', error='Only letters are allowed.'))
    postcode = fields.String(required=True, validate=Regexp('^[0-9a-zA-Z]+$', error='Only numbers and letters are allowed.'))
    class Meta:
        fields = ('id', 'street_number', 'street_name', 'suburb', 'postcode', 'user_id', 'user')
        ordered = True