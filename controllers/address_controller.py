from flask import Blueprint, request
from init import db
from models.address import Address, AddressSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

address_bp = Blueprint('addresses', __name__, url_prefix='/addresses')

# create address: all users can add their addresses to their account.
@address_bp.route('/', methods=['POST'])
@jwt_required()
def add_address():
    info = AddressSchema().load(request.json)
    address = Address(
        street_number = info['street_number'],
        street_name = info['street_name'],
        suburb = info['suburb'],
        postcode = info['postcode'],
        user_id = get_jwt_identity()
    )

    db.session.add(address)
    db.session.commit()
    return AddressSchema().dump(address), 201

# read addresses: all users can see the addresses they added for themselves
@address_bp.route('/')
@jwt_required()
def get_addresses():
    stmt = db.select(Address).filter_by(user_id=get_jwt_identity())
    addresses = db.session.scalars(stmt)
    return AddressSchema(many=True).dump(addresses)

# read addresses: all users can filter their addresses by entering address id.
@address_bp.route('/<int:id>/')
@jwt_required()
def get_an_address(id):
    stmt = db.select(Address).filter_by(user_id=get_jwt_identity(),id=id)
    addresses = db.session.scalars(stmt)
    return AddressSchema(many=True).dump(addresses)

# update address: all users can update their own address by address id
@address_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_address(id):
    stmt = db.select(Address).filter_by(user_id=get_jwt_identity(),id=id)
    address = db.session.scalar(stmt)
    info = AddressSchema().load(request.json, partial=True)

    if address:
        address.street_number = info.get('street_number') or address.street_number
        address.street_name = info.get('street_name') or address.street_name
        address.suburb = info.get('suburb') or address.suburb
        address.postcode = info.get('postcode') or address.postcode

        db.session.commit()
        return AddressSchema().dump(address)
    else:
        return {'error': f'Address with id {id} not found in your account.'}, 404

# delete address: all users can delete their own address by address id
@address_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_address(id):
    stmt = db.select(Address).filter_by(user_id=get_jwt_identity(),id=id)
    address = db.session.scalar(stmt)

    if address:
        db.session.delete(address)
        db.session.commit()
        return {'message': 'Address deleted successfully.'}
    else:
        return {'error': f'Address with id {id} not found in your account.'}, 404