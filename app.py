#!/bin/env python
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import os
from db import db
from datetime import timedelta
from security import authenticate, identity as identity_function
from resources.user import UserRegister
from resources.item import ItemList, Item
from resources.store import Store, StoreList


def main():
    os.environ['FLASK_ENV'] = 'development'

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "rX2D6Iwn*9zfyf!K"
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=7200)
    app.config['JWT_AUTH_URL_RULE'] = '/login'  # default /auth
    app.config['JWT_AUTH_USERNAME_KEY'] = 'username'  # default username
    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    jwt = JWT(app, authenticate, identity_function)  # /auth

    api.add_resource(ItemList, '/items')
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(UserRegister, '/register')
    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(StoreList, '/stores')

    db.init_app(app)
    app.run(port=5000, debug=True)


# This now requires a callback function
# @JWT.auth_response_handler
# def customized_response_handler(access_token, identity):
#    return jsonify({
#        'access_token': access_token.decode('utf-8'),
#        'user_id': identity.id
#    })

# This now requires a callback function
# @JWT.jwt_error_handler
# def customized_error_handler(error):
#    return jsonify({
#        'message': error.description,
#        'code': error.status_code
#    }), error.status_code

if __name__ == '__main__':
    main()