from flask import Blueprint, request
from init import db
from models.product import Category, CategorySchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize

category_bp = Blueprint('categories', __name__, url_prefix='/categories')

# create a category: only admin users can create a new category
@category_bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    authorize()
    category = Category(
        name = request.json['name']
    )
    db.session.add(category)
    db.session.commit()
    return CategorySchema().dump(category), 201

# read categories: all users can view a list of all categories.
@category_bp.route('/')
@jwt_required()
def get_categories():
    stmt = db.select(Category)
    categories = db.session.scalars(stmt)
    return CategorySchema(many=True).dump(categories)

# read a category: all users can view a certain category by providing a category id.
@category_bp.route('/<int:id>')
@jwt_required()
def get_a_category(id):
    stmt = db.select(Category).filter_by(id=id)
    category = db.session.scalar(stmt)
    if category:
        return CategorySchema().dump(category)
    else:
        return {'error': f'Category with id {id} not found.'}, 404

# update categories: only admin users can update category info.
@category_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_category(id):
    authorize()
    stmt = db.select(Category).filter_by(id=id)
    category = db.session.scalar(stmt)
    if category:
        category.name = request.json['name']
        db.session.commit()
        return CategorySchema().dump(category)
    else:
        return {'error': f'Category with id {id} not found.'}, 404

# delete a category: only admin users can delete a category.
@category_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    authorize()
    stmt = db.select(Category).filter_by(id=id)
    category = db.session.scalar(stmt)
    if category:
        db.session.delete(category)
        db.session.commit()
        return {'message': f'Category "{category.name}" deleted successfully.'}
    else:
        return {'error': f'Category with id {id} not found.'}, 404
