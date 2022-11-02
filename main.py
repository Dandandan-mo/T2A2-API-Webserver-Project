from flask import Flask
from init import db, ma, bcrypt, jwt
import os
from controllers.auth_controller import auth_bp
from controllers.cli_controller import db_bp

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEY'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    # errorhandlers

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(db_bp)
    
    @app.route('/')
    def index():
        return {"message": "Welcome to the C2C ecommerce app!"}

    return app
