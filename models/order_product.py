from init import db, ma
from marshmallow import fields
from marshmallow.validate import Range
from sqlalchemy.ext.hybrid import hybrid_property

class OrderProduct(db.Model):
    __tablename__ = 'order_products'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True, nullable=False)

    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    @hybrid_property
    def subtotal(self):
        return self.price * self.quantity

    order = db.relationship('Order', back_populates='order_products')
    product = db.relationship('Product', back_populates='order_products')

class OrderProductSchema(ma.Schema):
    product = fields.Nested('ProductSchema', only=['name'])

    product_id = fields.Integer(required=True, validate=Range(min=1, min_inclusive=True, error='Product id must be a positive integer.'))
    quantity = fields.Integer(required=True, validate=Range(min=1, min_inclusive=True, error='The mininum quantity is 1.'))

    class Meta:
        fields = ('order_id', 'product_id', 'product', 'price', 'quantity', 'subtotal')
        ordered = True