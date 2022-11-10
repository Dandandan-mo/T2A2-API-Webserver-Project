from flask import Blueprint, request, abort
from init import db
from datetime import date
from models.product import Product
from models.order import Order, OrderSchema
from models.order_product import OrderProduct, OrderProductSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('orders', __name__, url_prefix='/orders')

# create an order: all users can create an order by entering the id and quantity of the first product they want to purchase.
@order_bp.route('/new_order/', methods=['POST'])
@jwt_required()
def create_order():
    data = OrderProductSchema().load(request.json)
    order = Order(
        date = date.today(),
        user_id = get_jwt_identity()
    )
    db.session.add(order)
    db.session.commit()

    check_and_update_quantity(data)
    add_product_to_order(order, data)
    return OrderSchema().dump(order), 201
  
# add more order products: users can add more products to an existing order.
@order_bp.route('/<int:id>/add_product', methods=['POST'])
@jwt_required()
def add_order_product(id):
    data = OrderProductSchema().load(request.json, partial=True)
    stmt = db.select(Order).filter_by(id=id, user_id=get_jwt_identity())
    order = db.session.scalar(stmt)
    if not order:
        return {'error': f'You do not have an order with id {id}.'}, 404

    check_and_update_quantity(data)

    stmt = db.select(OrderProduct).filter_by(order_id=id, product_id=data['product_id'])
    order_product = db.session.scalar(stmt)
    if not order_product:
        add_product_to_order(order, data)
    else:
        order_product.quantity += data['quantity']
        db.session.commit()
    return OrderSchema().dump(order), 201

# update order products: users can adjust quantities of product they selected.
@order_bp.route('/<int:id>/update', methods=['PUT', 'PATCH'])
@jwt_required()
def update_order_product(id):
    data = OrderProductSchema().load(request.json, partial=True)
    stmt = db.select(Order).filter_by(id=id, user_id=get_jwt_identity())
    order = db.session.scalar(stmt)
    if not order:
        return {'error': f'You do not have an order with id {id}.'}, 404

    stmt = db.select(Product).filter_by(id=data['product_id'])
    product = db.session.scalar(stmt)
    if not product:
        return {'error': f"Product with id {data['product_id']} not found."}, 404

    stmt = db.select(OrderProduct).filter_by(order_id=id, product_id=data['product_id'])
    order_product = db.session.scalar(stmt)
    if not order_product:
        return {'error': f"Product with id {data['product_id']} is not in your order {id}."}, 404
    else:
        product.quantity += order_product.quantity
        if product.quantity >= data['quantity']:
            order_product.quantity = data['quantity']
            product.quantity -= data['quantity']
            db.session.commit()
            return OrderSchema().dump(order)
        else:
            abort(400, 'Requested quantity larger than avaiable quantity.')


# read orders: all users can view their orders
@order_bp.route('/')
@jwt_required()
def get_orders():
    stmt = db.select(Order).filter_by(user_id=get_jwt_identity()).order_by(Order.id.desc())
    orders = db.session.scalars(stmt)
    return OrderSchema(many=True).dump(orders)

# read a certain order: all users can view details of a certain order by providing the order id.
@order_bp.route('/<int:id>/')
@jwt_required()
def get_an_order(id):
    stmt = db.select(Order).filter_by(id=id, user_id=get_jwt_identity())
    order = db.session.scalar(stmt)
    if not order:
        return {'error': f'You do not have an order with id {id}.'}, 404
    return OrderSchema().dump(order)

# delete order_products: all users can delete products in an order
@order_bp.route('/<int:id>/del_product/', methods=['DELETE'])
@jwt_required()
def delete_a_product(id):
    stmt = db.select(Order).filter_by(id=id, user_id=get_jwt_identity())
    order = db.session.scalar(stmt)
    if not order:
        return {'error': f'You do not have an order with id {id}.'}, 404
    
    data = OrderProductSchema().load(request.json, partial=True)
    stmt = db.select(OrderProduct).filter_by(order_id=id, product_id=data['product_id'])
    order_product = db.session.scalar(stmt)
    if not order_product:
        return {'error': f"Product not found with id {data['product_id']}."}, 404
    db.session.delete(order_product)

    stmt = db.select(Product).filter_by(id=data['product_id'])
    product = db.session.scalar(stmt)
    product.quantity += order_product.quantity

    db.session.commit()
    return OrderSchema().dump(order)
    
# delete an order: all users can delete their own order history
@order_bp.route('/<int:id>/del', methods=["DELETE"])
@jwt_required()
def delete_order(id):
    stmt = db.select(Order).filter_by(id=id, user_id=get_jwt_identity())
    order = db.session.scalar(stmt)
    db.session.delete(order)
    db.session.commit()
    return {'message': f'Order {id} deleted successfully.'}

def add_product_to_order(order, data):
    stmt = db.select(Product).filter_by(id=data['product_id'])
    product = db.session.scalar(stmt)
    order_product = OrderProduct(
        order = order,
        product = product,
        price = product.price,
        quantity = data['quantity']
    )
    db.session.add(order_product)
    db.session.commit()
    
def check_and_update_quantity(data):
    stmt = db.select(Product).filter_by(id=data['product_id'])
    product = db.session.scalar(stmt)
    if not product:
        abort(404, f"Product not found with id {data['product_id']}.")
    if not product.quantity >= data['quantity']:
        abort(400, 'Requested quantity larger than avaiable quantity.')

    product.quantity -= data['quantity']
