from init import db, ma

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    addresses = db.relationship('Address', back_populates='user', cascade='all, delete')
    products = db.relationship('Product', back_populates='user', cascade='all, delete')
    orders = db.relationship('Order', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'is_admin')
        ordered = True