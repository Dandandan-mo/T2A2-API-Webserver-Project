from flask import Blueprint, request, abort
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

    check_and_update_quantity()
    add_product_to_order(order)
    return OrderSchema().dump(order), 201
  

# add more order_products: users can add more products to an existing order.
@order_bp.route('/<int:id>/', methods=['PUT'])
@jwt_required()
def update_order(id):
    stmt = db.select(Order).filter_by(id=id, user_id=get_jwt_identity())
    order = db.session.scalar(stmt)
    if not order:
        return {'error': f'You dn not have an order with id {id}.'}, 404

    check_and_update_quantity()
    
    stmt = db.select(OrderProduct).filter_by(order_id=id, product_id=request.json['product_id'])
    order_product = db.session.scalar(stmt)
    if not order_product:
        add_product_to_order(order)
    else:
        order_product.quantity += request.json['quantity']
        db.session.commit()
    return OrderSchema().dump(order), 201

# read orders: all users can view their orders
@order_bp.route('/')
@jwt_required()
def get_orders():
    stmt = db.select(Order).filter_by(user_id=get_jwt_identity()).order_by(Order.id.desc())
    orders = db.session.scalars(stmt)
    return OrderSchema(many=True).dump(orders)

# read a certain order: all users can view details of a certain order by providing the order id.

# update order_products: all users can update the quantities of the products added to the order

# delete order_products: all users can delete items in an order



def add_product_to_order(order):
    stmt = db.select(Product).filter_by(id=request.json['product_id'])
    product = db.session.scalar(stmt)
    order_product = OrderProduct(
        order = order,
        product = product,
        price = product.price,
        quantity = request.json['quantity']
    )
    
    db.session.add(order_product)
    db.session.commit()
    
def check_and_update_quantity():
    stmt = db.select(Product).filter_by(id=request.json['product_id'])
    product = db.session.scalar(stmt)
    if not product:
        abort(404, f"Product not found with id {request.json['product_id']}.")

    if not product.quantity >= request.json['quantity']:
        abort(400, 'Requested quantity larger than avaiable quantity.')

    product.quantity -= request.json['quantity']