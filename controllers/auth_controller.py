from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from datetime import timedelta
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register/', methods=['POST'])
def register_user():
    # validates and sanitise data using UserSchema
    data = UserSchema().load(request.json)
    try:
        # insert user data to the users table, add and commit the inserting
        user = User(
            email = data['email'],
            password = bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            phone_number = data['phone_number']
        )
        db.session.add(user)
        db.session.commit()

        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {"error": f"The email {request.json['email']} already in use."}, 409

@auth_bp.route('/login/', methods=['POST'])
def user_login():
    # get the user whose email matches the email entered
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    # if the user exist and the password matches the password stored in the users table, create an access token and return a message with email and token details.
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token}
    else:
        return {'error': 'Invalid email or password.'}, 401