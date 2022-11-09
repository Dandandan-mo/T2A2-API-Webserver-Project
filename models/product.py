from init import db, ma
from marshmallow import fields
from marshmallow.validate import And, Regexp, Length, Range, OneOf

VALID_CATEGORY = ['Electronics', 'Motors', 'Home', 'Garden', 'Clothing', 'Accessories', 'Sports', 'Health', 'Beauty', 'Other']

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='products')
    order_products = db.relationship('OrderProduct', back_populates='product', cascade='all, delete')

class ProductSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['first_name', 'last_name'])
    # category = fields.Nested('CategorySchema', only=['name'])

    name = fields.String(required=True, validate=And(Regexp("^[A-Za-z' ]+$", error='Only letters, spaces, and apostrophe are allowed.'),
    Length(min=2, error='Name must contain at least two characters.')
    ))
    description = fields.String(validate=Regexp("^[A-Za-z',.;: ]+$", error="Only letters, spaces, and certain characters(',.;:) are allowed."))
    category = fields.String(required=True, validate=OneOf(VALID_CATEGORY))
    quantity = fields.Integer(required=True, validate=Range(min=1, min_inclusive=True, error='The minimum quantity is 1.'))
    price = fields.Float(required=True, validate=Range(min=0, min_inclusive=True, error='The lowest price is 0.'))

    class Meta:
        fields = ('id', 'name', 'description', 'category', 'price', 'quantity', 'user_id', 'user')
        ordered = True