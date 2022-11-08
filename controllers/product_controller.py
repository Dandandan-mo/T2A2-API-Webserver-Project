from flask import Blueprint, request
from init import db
from models.product import Product, ProductSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

product_bp = Blueprint('products', __name__, url_prefix='/products')

# create product: all users can post their own product for sale.
@product_bp.route('/', methods=['POST'])
@jwt_required()
def add_product():
    data = ProductSchema().load(request.json)
    try:
        product = Product(
            name = data['name'],
            description = data.get('description'),
            quantity = data['quantity'],
            price = data['price'],
            user_id = get_jwt_identity(),
            category_id = data['category_id']
        )
        db.session.add(product)
        db.session.commit()
        return ProductSchema().dump(product)
    except IntegrityError:
        return {'error': 'Invalid category_id input.'}, 400

# read products: all users can browse all products for sale.
@product_bp.route('/')
@jwt_required()
def get_products():
    stmt = db.select(Product)
    products = db.session.scalars(stmt)
    return ProductSchema(many=True).dump(products)

# read produts: all users can filter products by categories
@product_bp.route('/category:<int:id>/')
@jwt_required()
def filter_products(id):
    stmt = db.select(Product).filter_by(category_id=id)
    products = db.session.scalars(stmt)
    return ProductSchema(many=True).dump(products)

# read a certain product: all users can view info of a certain product by providing a product id.
@product_bp.route('/<int:id>/')
@jwt_required()
def get_a_product(id):
    stmt = db.select(Product).filter_by(id=id)
    product = db.session.scalar(stmt)
    if product:
        return ProductSchema().dump(product)
    else:
        return {'error': f'Product not found with id {id}.'}, 404

# update a product: users can update products they posted.
@product_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_product(id):
    stmt = db.select(Product).filter_by(id=id, user_id=get_jwt_identity())
    product = db.session.scalar(stmt)
    data = ProductSchema().load(request.json, partial=True)
    if product:
        product.name = data.get('name') or product.name
        product.description = data.get('description') or product.description
        product.quantity = data.get('quantity') or product.quantity
        product.price = data.get('price') or product.price
        product.category_id = data.get('category_id') or product.category_id

        db.session.commit()
        return ProductSchema().dump(product)
    else:
        return {'error': f'You do not have a product with id {id}'}, 404

# delete a product: users can delete products they posted.
@product_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    stmt = db.select(Product).filter_by(id=id, user_id=get_jwt_identity())
    product = db.session.scalar(stmt)
    if product:
        db.session.delete(product)
        db.session.commit()
        return {'message': f'Product "{product.name}" deleted successfully.'}
    else:
        return {'error': f'You do not have a product with id {id}'}, 404