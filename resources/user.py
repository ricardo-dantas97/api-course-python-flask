from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blocklist import BLOCKLIST


arguments = reqparse.RequestParser()
arguments.add_argument('login', type=str, required=True, help="This field cannot be empty.")
arguments.add_argument('senha', type=str, required=True, help="This field cannot be empty.")


class Users(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json(), 200
        return {'message': 'User ID not found'}, 400
    

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to save user.'}, 500
            return {'message': 'User deleted.'}
        return {'message': 'User ID not found.'}, 400


class UsersRegister(Resource):
    def post(self):
        data = arguments.parse_args()

        if UserModel.find_by_login(data['login']):
            return {'message': 'This login already exists.'}, 401
        
        user = UserModel(**data)
        user.save_user()
        return {'message': 'User created successfully.', 'data': user.json()}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = arguments.parse_args()

        user = UserModel.find_by_login(data['login'])
        if user and user.senha == data['senha']:
            token = create_access_token(identity=user.user_id)
            return {'access_token': token}, 200
        return {'message':'The login or password is not correct.'}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLOCKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}, 200