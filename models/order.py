from init import db, ma
from marshmallow import fields
from sqlalchemy.ext.hybrid import hybrid_property

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @hybrid_property
    def total_payable(self):
        total = 0
        for order_product in self.order_products:
            total += order_product.subtotal
        return total

    user = db.relationship('User')
    order_products = db.relationship('OrderProduct', back_populates='order', cascade='all, delete')

class OrderSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['first_name', 'last_name'])
    order_products = fields.List(fields.Nested('OrderProductSchema', exclude=['order_id']))

    class Meta:
        fields = ('id', 'date', 'user_id', 'user', 'order_products', 'total_payable')
        ordered = True

