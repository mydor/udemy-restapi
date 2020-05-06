from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.item import ItemModel


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        claims = get_jwt_claims()
        items = [x.json() for x in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {'items': [x['name'] for x in items],
                'message': 'More data available if you log in.'
                }, 200


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")
    parser.add_argument('store_id', type=int, required=True, help="This field cannot be left blank")

    @jwt_required
    def get(self, name):  # cRud

        item = ItemModel.find_by_name(name)
        if item:
            return {'item': item.json()}, 200

        return {'item': item}, 404

    @jwt_required
    def post(self, name):  # Crud
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists'}, 400

        data = self.__class__.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.store_item()
        except Exception:
            return {"message": f"An error occurred inserting {name}"}, 500

        return item.json(), 201

    @jwt_required
    def put(self, name):  # crUd
        data = self.__class__.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
            item.store_id = data['store_id']
            code = 202
        else:
            item = ItemModel(name, **data)
            code = 201

        item.store_item()
        return item.json(), code

    @fresh_jwt_required
    def delete(self, name):  # cruD
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)
        if not item:
            return {'message': f'An item with name {name} was not found'}, 404

        item.delete_item()
        return {'message': f'Item {name} has been deleted'}, 200
