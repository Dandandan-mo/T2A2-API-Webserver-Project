from init import db, bcrypt
from datetime import datetime
from flask import Blueprint
from models.user import User
from models.address import Address
from models.product import Product
from models.order import Order, OrderProduct

db_bp = Blueprint('db', __name__)

@db_bp.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created.')

@db_bp.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables dropped.')

@db_bp.cli.command('seed')
def seed_db():
    users = [
        User(
            email = 'firstuser@email.com',
            password = bcrypt.generate_password_hash('password234').decode('utf-8'),
            first_name = 'Jimmy',
            last_name = 'OYang',
            phone_number = '0432000001'
        ),
        User(
            email = 'seconduser@email.com',
            password = bcrypt.generate_password_hash('password567').decode('utf-8'),
            first_name = 'Ali',
            last_name = "Wong",
            phone_number = "0430000021"
        )
    ]
    db.session.add_all(users)
    db.session.commit()

    addresses = [
        Address(
            street_number = '11',
            street_name = 'Nicolson St',
            suburb = 'Calten',
            postcode = '3053',
            user = users[0]
        ),
        Address(
            street_number = '1',
            street_name = 'Flemmingten Rd',
            suburb = 'Purkvile',
            postcode = '3052',
            user = users[1]
        )
    ]
    db.session.add_all(addresses)

    products = [
        Product(
            name = 'Apple iPhone 11',
            description = 'As new condition, 64GB, without contract.',
            category = 'Electronics',
            quantity = 3,
            price = 478.5,
            user = users[0]
        ),
        Product(
            name = 'Single Bunk Bed',
            description = 'Solid wooden bed frame, brand-new item in its original packaging; color: white; height: 152.2 cm.',
            category = 'Home & Garden',
            quantity = 15,
            price = 425,
            user = users[0]
        ),
        Product(
            name = 'Mesh Beach Tote Bag',
            description = 'Lightweight bag made of Polyester, foldable and fast drying, perfect for travel.',
            category = 'Clothing & Accessories',
            quantity = 5,
            price = 20.25,
            user = users[1]
        ),
        Product(
            name = 'Long Raincoat',
            description = 'Men waterproof black hooded trench jacket for outdoor hiking. Size L.',
            category = 'Clothing & Accessories',
            quantity = 2,
            price = 24,
            user = users[1]
        )
    ]
    db.session.add_all(products)

    orders = [
        Order(
            date = datetime.strptime('11-01-22', '%m-%d-%y').date(),
            user = users[0]
        ),
        Order(
            date = datetime.strptime('11-02-22', '%m-%d-%y').date(),
            user = users[1]
        )
    ]
    db.session.add_all(orders)
    db.session.commit()

    order_products = [
        OrderProduct(
            order = orders[0],
            product = products[0],
            price = 478.5,
            quantity = 1
        ),
        OrderProduct(
            order = orders[1],
            product = products[2],
            price = 20.25,
            quantity = 1
        )
    ]
    db.session.add_all(order_products)
    db.session.commit()

    print('Tables seeded')