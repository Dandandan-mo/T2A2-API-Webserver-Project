from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from datetime import timedelta
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register/', methods=['POST'])
def register_user():
    try:
        user = User(
            username = request.json['username'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
            first_name = request.json.get('first_name'),
            last_name = request.json.get('last_name'),
            phone_number = request.json['phone_number']
        )
        db.session.add(user)
        db.session.commit()

        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {"error": f"The username {request.json['username']} already in use."}, 409

@auth_bp.route('/login/', methods=['POST'])
def user_login():
    stmt = db.select(User).filter_by(username=request.json['username'])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'username': user.username, 'token': token}
    else:
        return {'error': 'Invalid username or password.'}, 401