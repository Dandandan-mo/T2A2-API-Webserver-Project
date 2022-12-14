from init import db, bcrypt
from datetime import datetime
from flask import Blueprint
from models.user import User
from models.address import Address
from models.product import Product
from models.order import Order
from models.order_product import OrderProduct

db_bp = Blueprint('db', __name__)

@db_bp.cli.command('create')
def create_db():
    # create all tables
    db.create_all()
    print('Tables created.')

@db_bp.cli.command('drop')
def drop_db():
    # drop all tables
    db.drop_all()
    print('Tables dropped.')

@db_bp.cli.command('seed')
def seed_db():
    # insert a list of user data into the users table, add them all and commit them into database
    users = [
        User(
            email = 'firstuser@email.com',
            password = bcrypt.generate_password_hash('Password234!').decode('utf-8'),
            first_name = 'Jimmy',
            last_name = 'OYang',
            phone_number = '0432000001'
        ),
        User(
            email = 'seconduser@email.com',
            password = bcrypt.generate_password_hash('Password567@').decode('utf-8'),
            first_name = 'Ali',
            last_name = "Wong",
            phone_number = "0430000021"
        )
    ]
    db.session.add_all(users)
    db.session.commit()
    
    # insert a list of address data to the addresses table, add the inserting
    addresses = [
        Address(
            street_number = '11',
            street_name = 'Nicolson St',
            suburb = 'Calten',
            postcode = '3053',
            user_id = users[0].id
        ),
        Address(
            street_number = '1',
            street_name = 'Flemmingten Rd',
            suburb = 'Purkvile',
            postcode = '3052',
            user_id = users[1].id
        )
    ]
    db.session.add_all(addresses)

    # insert a list of product data into the products table, add the inserting 
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
            category = 'Home',
            quantity = 15,
            price = 425,
            user = users[0]
        ),
        Product(
            name = 'Mesh Beach Tote Bag',
            description = 'Lightweight bag made of Polyester, foldable and fast drying, perfect for travel.',
            category = 'Accessories',
            quantity = 5,
            price = 20.25,
            user = users[1]
        ),
        Product(
            name = 'Long Raincoat',
            description = 'Men waterproof black hooded trench jacket for outdoor hiking. Size L.',
            category = 'Clothing',
            quantity = 2,
            price = 24,
            user = users[1]
        )
    ]
    db.session.add_all(products)

    # insert a list of order data into the orders table, add the inserting orders and commit all changes since last commit
    orders = [
        Order(
            date = datetime.strptime('11-01-22', '%m-%d-%y').date(),
            user_id = users[0].id
        ),
        Order(
            date = datetime.strptime('11-02-22', '%m-%d-%y').date(),
            user_id = users[1].id
        )
    ]
    db.session.add_all(orders)
    db.session.commit()

    # insert a list of order_product into the order_products table, add and commit it to databse
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