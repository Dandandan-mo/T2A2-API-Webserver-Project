from flask import Blueprint, request
from init import db
from datetime import date
from models.product import Product
from models.order import Order, OrderSchema, OrderProduct, OrderProductSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('orders', __name__, url_prefix='/orders')

# create an order: all users can create an order by entering the id and quantity of the first product they want to purchase.
@order_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    order = Order(
        date = date.today(),
        user_id = get_jwt_identity()
    )
    db.session.add(order)
    db.session.commit()

    add_product_to_order(order)
    return OrderSchema().dump(order), 201

# create more order_products: users can add more products to an existing order.
@order_bp.route('/<int:id>', methods=['POST'])
@jwt_required()
def update_order(id):
    stmt = db.select(Order).filter_by(id=id, user_id=get_jwt_identity())
    order = db.session.scalar(stmt)
    if not order:
        return {'error': f'You dn not have an order with id {id}.'}, 404

    add_product_to_order(order)
    return OrderSchema().dump(order), 201

# read order: all users can view their orders

# delete order_products: all users can delete items in an order

def add_product_to_order(order):
    stmt = db.select(Product).filter_by(id=request.json['product_id'])
    product = db.session.scalar(stmt)
    if not product:
        return {'error': f"Product not found with id {request.json['product_id']} in this order."}, 404
    if not product.quantity >= request.json['quantity']:
        return {'error': 'Requested quantity larger than avaiable quantity.'}, 400
    product.quantity -= request.json['quantity']

    order_product = OrderProduct(
        order = order,
        product = product,
        price = product.price,
        quantity = request.json['quantity']
    )
    
    db.session.add(order_product)
    db.session.commit()