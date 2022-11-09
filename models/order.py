from init import db, ma
from marshmallow import fields

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='orders')
    order_products = db.relationship('OrderProduct', back_populates='order', cascade='all, delete')
    # payment = db.relationship('Payment', back_populates='order', cascade= 'all, delete')
    # shipment = db.relationship('Shipment', back_populates='order', cascade='all, delete')

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

