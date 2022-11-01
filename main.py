from flask import Flask
from init import db, ma, bcrypt, jwt
import os

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
    @app.route('/')
    def index():
        return {"message": "Welcome to the C2C ecommerce app!"}

    return app


