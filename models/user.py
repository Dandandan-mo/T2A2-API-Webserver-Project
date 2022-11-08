from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String, nullable=False)
    
    addresses = db.relationship('Address', back_populates='user', cascade='all, delete')
    products = db.relationship('Product', back_populates='user', cascade='all, delete')
    orders = db.relationship('Order', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    products = fields.List(fields.Nested('ProductSchema', exclude=['user_id', 'user']))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=And(
        Length(min=6, error='Password must be at least 6 characters long.'),
        Regexp('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W]).*$', error='Password must inlcude at least one uppercase letter, one lowercase letter, one digit and one non-word character.')
    ))
    phone_number = fields.String(required=True, validate=And(
        Length(min=7, max=15, error='Phone number must be 7-15 digits long.'),
        Regexp('^[0-9]+$', error='Only digits are allowed.')
    ))
    first_name = fields.String(validate=Regexp('^[A-Za-z]+$', error='Only letters are allowed.'))
    last_name = fields.String(validate=Regexp('^[A-Za-z]+$', error='Only letters are allowed.'))

    class Meta:
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'products')
        ordered = True