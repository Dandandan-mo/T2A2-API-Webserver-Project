from init import db, ma
from marshmallow import fields
from marshmallow.validate import Range

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='orders')
    order_products = db.relationship('OrderProduct', back_populates='order', cascade='all, delete')
    # payment = db.relationship('Payment', back_populates='order', cascade= 'all, delete')
    # shipment = db.relationship('Shipment', back_populates='order', cascade='all, delete')

class OrderProduct(db.Model):
    __tablename__ = 'order_products'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True, nullable=False)

    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', back_populates='order_products')
    product = db.relationship('Product', back_populates='order_products')


class OrderSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['first_name', 'last_name'])
    order_products = fields.List(fields.Nested('OrderProductSchema', exclude=['order_id']))

    # total_payable = fields.Method("calc_total_payable")

    # def calc_total_payable(self, order):
    #     total = 0
    #     for product in order.order_products:
    #         total += product['payable']
    #         return total

    class Meta:
        fields = ('id', 'date', 'user_id', 'user', 'order_products')
        ordered = True

class OrderProductSchema(ma.Schema):
    product = fields.Nested('ProductSchema', only=['name'])
    payable = fields.Function(lambda order_product: order_product.price * order_product.quantity)
    product_id = fields.Integer(required=True, validate=Range(min=1, min_inclusive=True, error='Product id must be a positive integer.'))
    quantity = fields.Integer(required=True, validate=Range(min=1, min_inclusive=True, error='The mininum quantity is 1.'))

    class Meta:
        fields = ('order_id', 'product_id', 'product', 'price', 'quantity', 'payable')
        ordered = True