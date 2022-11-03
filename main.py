from flask import Flask
from init import db, ma, bcrypt, jwt
import os
from controllers.auth_controller import auth_bp
from controllers.cli_controller import db_bp
from controllers.user_controller import user_bp
from controllers.address_controller import address_bp

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEYS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    # errorhandlers
    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error': f'The field {err} is required.'}, 500

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(db_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(address_bp)
    
    @app.route('/')
    def index():
        return {"message": "Welcome to the C2C ecommerce app!"}

    return app
