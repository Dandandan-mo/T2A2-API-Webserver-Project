from init import db, ma
from marshmallow import fields

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='orders')
    order_products = db.relationship('OrderProduct', back_populates='order', cascade='all, delete')
    payment = db.relationship('Payment', back_populates='order', cascade= 'all, delete')
    shipment = db.relationship('Shipment', back_populates='order', cascade='all, delete')

class OrderProduct(db.Model):
    __tablename__ = 'order_products'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True, nullable=False)

    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', back_populates='order_products')
    product = db.relationship('Product', back_populates='order_products')



class OrderSchema(ma.Schema):
    user = fields.Nested('User', only=['first_name', 'last_name'])
    order_products = fields.List(fields.Nested('OrderProduct', exclude=['order_id']))
    class Meta:
        fields = ('id', 'date', 'user_id', 'user', 'order_products')

class OrderProductSchema(ma.Schema):
    total_price = fields.Function(lambda product_orders: sum(product_orders.price * product_orders.quantity))

    class Meta:
        fields = ('order_id', 'product_id', 'price', 'quantity', 'total_price')