from init import db, ma
from marshmallow import fields

class Shipment(db.Model):
    __tablename__ = 'shipments'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)

    order = db.relationship('Order', back_populates='shipment')
    address = db.relationship('Address', back_populates='shipment')

class ShipmentSchema(ma.Schema):
    address = fields.Nested('Address')
    class Meta:
        fields = ('id', 'date', 'order_id', 'address_id', 'address')
        ordered = True
