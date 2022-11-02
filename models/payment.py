from init import db, ma 

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date= db.Column(db.Date, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    order = db.relationship('Order', back_populates='payment')

class PaymentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'type', 'amount', 'date', 'order_id')
        ordered = True