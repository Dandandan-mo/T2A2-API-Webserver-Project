from flask import Blueprint, request
from init import db
from models.address import Address, AddressSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

address_bp = Blueprint('addresses', __name__, url_prefix='/addresses')

# create address: all users can add their addresses to their account.
@address_bp.route('/', methods=['POST'])
@jwt_required()
def add_address():
    address = Address(
        tag = request.json.get('tag'),
        street_number = request.json['street_number'],
        street_name = request.json['street_name'],
        suburb = request.json['suburb'],
        postcode = request.json['postcode'],
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

# read addresses: all users can filter their addresses based on tags
@address_bp.route('/<string:tag>/')
@jwt_required()
def get_an_address(tag):
    stmt = db.select(Address).filter_by(user_id=get_jwt_identity(),tag=tag)
    addresses = db.session.scalars(stmt)
    return AddressSchema(many=True).dump(addresses)

# update address: all users can update their own address by address id
@address_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_address(id):
    stmt = db.select(Address).filter_by(user_id=get_jwt_identity(),id=id)
    address = db.session.scalar(stmt)

    if address:
        address.tag = request.json.get('tag') or address.tag
        address.street_number = request.json.get('street_number') or address.street_number
        address.street_name = request.json.get('street_name') or address.street_name
        address.suburb = request.json.get('suburb') or address.suburb
        address.postcode = request.json.get('postcode') or address.postcode

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