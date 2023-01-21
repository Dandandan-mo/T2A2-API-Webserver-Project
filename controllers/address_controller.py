from flask import Blueprint, request
from init import db
from models.address import Address, AddressSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

address_bp = Blueprint('addresses', __name__, url_prefix='/addresses')

@address_bp.route('/new_addr', methods=['POST'])
@jwt_required()
def add_address():
     # validates and sanitise data using AddressSchema
    data = AddressSchema().load(request.json)
    # insert address data into the addresses table, add and commit it to databse, return the newly inserted address.
    address = Address(
        street_number = data['street_number'],
        street_name = data['street_name'],
        suburb = data['suburb'],
        postcode = data['postcode'],
        user_id = get_jwt_identity()
    )

    db.session.add(address)
    db.session.commit()
    return AddressSchema().dump(address), 201

@address_bp.route('/')
@jwt_required()
def get_addresses():
    # get the list of addresses whose user_id matches the identity of the user logged in
    stmt = db.select(Address).filter_by(user_id=get_jwt_identity())
    addresses = db.session.scalars(stmt)
    return AddressSchema(many=True).dump(addresses)

@address_bp.route('/<int:id>/')
@jwt_required()
def get_an_address(id):
    # get the particular address whose id matches the id provided and user_id matches the identity of the user logged in.
    stmt = db.select(Address).filter_by(user_id=get_jwt_identity(),id=id)
    addresses = db.session.scalars(stmt)
    return AddressSchema(many=True).dump(addresses)

@address_bp.route('/<int:id>/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_address(id):
    # get the particular address whose id matches the id provided and user_id matches the identity of the user logged in.
    stmt = db.select(Address).filter_by(user_id=get_jwt_identity(),id=id)
    address = db.session.scalar(stmt)
     # validates and sanitise data using AddressSchema
    data = AddressSchema().load(request.json, partial=True)
    
    # if the address exist, update the address data in the addresses table and commit the change, return the updated address
    if address:
        address.street_number = data.get('street_number') or address.street_number
        address.street_name = data.get('street_name') or address.street_name
        address.suburb = data.get('suburb') or address.suburb
        address.postcode = data.get('postcode') or address.postcode

        db.session.commit()
        return AddressSchema().dump(address)
    else:
        return {'error': f'You do not have an address with id {id}.'}, 404

@address_bp.route('/<int:id>/del', methods=['DELETE'])
@jwt_required()
def delete_address(id):
    # get the particular address whose id matches the id provided and user_id matches the identity of the user logged in.
    stmt = db.select(Address).filter_by(user_id=get_jwt_identity(),id=id)
    address = db.session.scalar(stmt)
    # if address exist, delete the address and commit the change, return an success message, else return an error message.
    if address:
        db.session.delete(address)
        db.session.commit()
        return {'message': f'Address {id} deleted successfully.'}
    else:
        return {'error': f'You do not have an address with id {id}.'}, 404