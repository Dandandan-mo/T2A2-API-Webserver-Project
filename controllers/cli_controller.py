from init import db, bcrypt
from datetime import date
from flask import Blueprint
from models.user import User
from models.address import Address

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
            username = 'firstuser@email.com',
            password = bcrypt.generate_password_hash('password234').decode('utf-8'),
            first_name = 'Jimmy',
            last_name = 'OYang',
            phone_number = '0432000001'
        ),
        User(
            username = 'seconduser@email.com',
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
    db.commit()

    # keep adding basic data for all the entities
    
    print('Tables seeded')