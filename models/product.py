from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    products = db.relationship('Product', back_populates='category', cascade='all, delete')

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    user = db.relationship('User', back_populates='products')
    category = db.relationship('Category', back_populates='products')
    order_products = db.relationship('OrderProduct', back_populates='product', cascade='all, delete')

class CategorySchema(ma.Schema):
    name = fields.String(required=True, validate=Regexp("^[A-Za-z' ]+$", error='Only letters and spaces and certain characters are allowed.'))
    class Meta:
        fields = ('id', 'name')

class ProductSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['email'])
    category = fields.Nested('CategorySchema', only=['name'])

    # @validates('quantity')
    # def validate_quantity(self, value):
    #     if value < 0:
    #         raise ValidationError()

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity', 'user_id', 'category_id','category', 'user')
        ordered = True