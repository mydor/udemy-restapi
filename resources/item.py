from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")
    parser.add_argument('store_id', type=int, required=True, help="This field cannot be left blank")

    @jwt_required()
    def get(self, name):  # cRud

        item = ItemModel.find_by_name(name)
        if item:
            return {'item': item.json()}, 200

        return {'item': item}, 404

    @jwt_required()
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

    @jwt_required()
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

    @jwt_required()
    def delete(self, name):  # cruD
        item = ItemModel.find_by_name(name)
        if not item:
            return {'message': f'An item with name {name} was not found'}, 404

        item.delete_item()
        return {'message': f'Item {name} has been deleted'}, 200
