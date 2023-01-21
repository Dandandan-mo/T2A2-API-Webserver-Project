from flask import Blueprint, request, abort
from init import db
from datetime import date
from models.product import Product
from models.order import Order, OrderSchema
from models.order_product import OrderProduct, OrderProductSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

order_bp = Blueprint('orders', __name__, url_prefix='/orders')

@order_bp.route('/new_order/', methods=['POST'])
@jwt_required()
def create_order():
    # validates and sanitise data using OrderProductSchema
    data = OrderProductSchema().load(request.json)
    # insert a record of order to the orders table and add and commit the change to database
    order = Order(
        date = date.today(),
        user_id = get_jwt_identity()
    )
    db.session.add(order)
    db.session.commit()

    # get the product whose id matches the product id entered.
    stmt = db.select(Product).filter_by(id=data['product_id'])
    product = db.session.scalar(stmt)
    if not product:
        abort(404, f"Product not found with id {data['product_id']}.")

    check_and_update_quantity(product, data)
    add_product_to_order(order, data)
    # return the order.
    return OrderSchema().dump(order), 201
  
@order_bp.route('/<int:id>/add_product', methods=['POST'])
@jwt_required()
def add_order_product(id):
    # validates and sanitise data using OrderProductSchema
    data = OrderProductSchema().load(request.json, partial=True)
    # get the order that has the provided id and the user_id that matches the identity of the currently logged in user
    stmt = db.select(Order).filter_by(id=id, user_id=get_jwt_identity())
    order = db.session.scalar(stmt)
    if not order:
        return {'error': f'You do not have an order with id {id}.'}, 404
    
    try:
        stmt = db.select(Product).filter_by(id=data['product_id'])
        product = db.session.scalar(stmt)
        if not product:
            abort(404, f"Product not found with id {data['product_id']}.")
            
        check_and_update_quantity(product, data)
        add_product_to_order(order, data)
        return OrderSchema().dump(order), 201
    except IntegrityError:
        return {'error': 'Please check if this product is already added.'}

@order_bp.route('/<int:id>/update', methods=['PUT', 'PATCH'])
@jwt_required()
def update_order_product(id):
      # validates and sanitise data using OrderProductSchema
    data = OrderProductSchema().load(request.json, partial=True)
    # get the order whose id matches the provided id and user_id matches identity of the logged in user
    stmt = db.select(Order).filter_by(id=id, user_id=get_jwt_identity())
    order = db.session.scalar(stmt)
    if not order:
        return {'error': f'You do not have an order with id {id}.'}, 404

    # get the order_product whose order id matches the provided id and product id matches the entered product id.
    stmt = db.select(OrderProduct).filter_by(order_id=id, product_id=data['product_id'])
    order_product = db.session.scalar(stmt)
    if not order_product:
        return {'error': f"Product with id {data['product_id']} is not in your order {id}."}, 404
    else:
        # update quantity of product in stock - put the selected order_product back to inventory
        stmt = db.select(Product).filter_by(id=data['product_id'])
        product = db.session.scalar(stmt)
        product.quantity += order_product.quantity
        order_product.quantity = data['quantity']

        check_and_update_quantity(product, data)
        db.session.commit()
        return OrderSchema().dump(order)

@order_bp.route('/')
@jwt_required()
def get_orders():
    # get a list of orders whose user_id matches the identity of the logged in user in the token ordered by descending id
    stmt = db.select(Order).filter_by(user_id=get_jwt_identity()).order_by(Order.id.desc())
    orders = db.session.scalars(stmt)
    return OrderSchema(many=True).dump(orders)


@order_bp.route('/<int:id>/')
@jwt_required()
def get_an_order(id):
    # get a specific order whose id matches the id provided and whose user_id matches the identity of the logged in user.
    stmt = db.select(Order).filter_by(id=id, user_id=get_jwt_identity())
    order = db.session.scalar(stmt)
    if not order:
        return {'error': f'You do not have an order with id {id}.'}, 404
    return OrderSchema().dump(order)

@order_bp.route('/<int:id>/del_product/', methods=['DELETE'])
@jwt_required()
def delete_a_product(id):
    # get the order whose id matches the id provided and whose user_id matches the identity of the user logged in
    stmt = db.select(Order).filter_by(id=id, user_id=get_jwt_identity())
    order = db.session.scalar(stmt)
    if not order:
        return {'error': f'You do not have an order with id {id}.'}, 404
     # validates and sanitise data using OrderProductSchema
    data = OrderProductSchema().load(request.json, partial=True)
    # get the order_produt whose order_id matches the id provided and whose product id matches the product id entered
    stmt = db.select(OrderProduct).filter_by(order_id=id, product_id=data['product_id'])
    order_product = db.session.scalar(stmt)
    if not order_product:
        return {'error': f"Product not found with id {data['product_id']} in your order {id}."}, 404
    # delete the order_product
    db.session.delete(order_product)

    # get the product with the product id provided
    stmt = db.select(Product).filter_by(id=data['product_id'])
    product = db.session.scalar(stmt)
    # update the quantity of the product in the products table.
    product.quantity += order_product.quantity
    # commit the changes to the database, return the order
    db.session.commit()
    return OrderSchema().dump(order)

def add_product_to_order(order, data):
    # insert a row to the order_products table in the database, and and commit the inserting.
    order_product = OrderProduct(
        order = order,
        product_id = data['product_id'],
        price = data['price'],
        quantity = data['quantity']
    )
    db.session.add(order_product)
    db.session.commit()
    
def check_and_update_quantity(product, data):
    # if the requested quantity is larger than product quantity in stock, return an error messsage
    if not product.quantity >= data['quantity']:
        abort(400, 'Requested quantity larger than avaiable quantity.')
    # update the quantity in the products table otherwise
    product.quantity -= data['quantity']
