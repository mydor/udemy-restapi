from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'store': store.json()}
        return {'message': f'Store {name} not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'Store {name} already exists.'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': f'An error occurred while creating store named {name}.'}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': f'Store {name} deleted'}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
