from init import db, ma
from marshmallow import fields 

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tag = db.Column(db.String)
    street_number = db.Column(db.String, nullable=False)
    street_name = db.Column(db.String, nullable=False)
    suburb = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User', back_populates='addresses')
    # shipments = db.relationship('Shipment', back_populates='address')

class AddressSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username', 'phone_number'])
    class Meta:
        fields = ('id', 'tag', 'street_number', 'street_name', 'suburb', 'postcode', 'user_id', 'user')
        ordered = True