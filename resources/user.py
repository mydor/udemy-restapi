import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    def post(self):
        data = self.__class__.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"User {data['username']} already exists."}, 400

        user = UserModel(**data)
        user.store_user()

        return {"message": f"User {user.username} created successfully."}, 201

