from flask import Blueprint, request
from init import db
from models.product import Product, ProductSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

product_bp = Blueprint('products', __name__, url_prefix='/products')

@product_bp.route('/new_product/', methods=['POST'])
@jwt_required()
def add_product():
    # validates and deserializes the input product info dictionary to an application-level data structure
    data = ProductSchema().load(request.json)
    # insert a record to the products table and commit the inserting. return the newly inserted product object
    product = Product(
        name = data['name'],
        description = data.get('description'),
        category = data['category'],
        quantity = data['quantity'],
        price = data['price'],
        user_id = get_jwt_identity()
    )
    db.session.add(product)
    db.session.commit()
    return ProductSchema().dump(product)

@product_bp.route('/')
@jwt_required()
def get_products():
    # retrieve a list of all products
    stmt = db.select(Product)
    products = db.session.scalars(stmt)
    return ProductSchema(many=True).dump(products)

@product_bp.route('/<string:category>/')
@jwt_required()
def filter_products(category):
    # get a list of products filtered by category name entered
    stmt = db.select(Product).filter_by(category=category)
    products = db.session.scalars(stmt)
    return ProductSchema(many=True).dump(products)


@product_bp.route('/<int:id>/')
@jwt_required()
def get_a_product(id):
    # retrieve certain product with the provided id
    stmt = db.select(Product).filter_by(id=id)
    product = db.session.scalar(stmt)
    if product:
        return ProductSchema().dump(product)
    else:
        return {'error': f'Product not found with id {id}.'}, 404

@product_bp.route('/<int:id>/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_product(id):
    # get the product with the provided id
    stmt = db.select(Product).filter_by(id=id, user_id=get_jwt_identity())
    product = db.session.scalar(stmt)
    if not product:
        return {'error': f'You do not have a product with id {id}'}, 404
    # validates and deserializes an input dictionary of product info to an application-level data structure
    data = ProductSchema().load(request.json, partial=True)
    # update the product info and commit it to database, return the updated product.
    product.name = data.get('name') or product.name
    product.description = data.get('description') or product.description
    product.category = data.get('category') or product.category
    product.quantity = data.get('quantity') or product.quantity
    product.price = data.get('price') or product.price

    db.session.commit()
    return ProductSchema().dump(product)

@product_bp.route('/<int:id>/del', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    # get the product that has the id provided and is posted by the user logged in
    stmt = db.select(Product).filter_by(id=id, user_id=get_jwt_identity())
    product = db.session.scalar(stmt)
    if not product:
        return {'error': f'You do not have a product with id {id}'}, 404
    # delete the product and commit it to database, return a success message.
    db.session.delete(product)
    db.session.commit()
    return {'message': f'Product "{product.name}" deleted successfully.'}