#!/bin/env python

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

import os
from datetime import timedelta
from resources.user import (
    UserRegister,
    User,
    UserLogin,
    UserLogout,
    TokenRefresh
)
from resources.item import ItemList, Item
from resources.store import Store, StoreList
from blacklist import BLACKLIST

os.environ['FLASK_ENV'] = 'development'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "rX2D6Iwn*9zfyf!K"
app.config['JWT_SECRET_KEY'] = 'BSr^7!s2v^F7Lff&'
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=5)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=1800)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=86400)
# app.config['JWT_AUTH_URL_RULE'] = '/login'  # default /auth
app.config['JWT_AUTH_USERNAME_KEY'] = 'username'  # default username
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

api = Api(app)

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claimes_to_jwt(identity):
    if identity == 1:
        return{'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(decrypted_token):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def unauthorized_token_callback():
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')


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
    app.run(port=5000, debug=True)
