from flask_restful import Resource
from app.decorators import auth_user, expect, is_role
from app.parsers import change_password_parser
from .user_service import UserService

user_service = UserService()

class Users(Resource):
    @auth_user
    @is_role('admin')
    def get(self, current_user):
        return user_service.get_all_logins()

class ChangePassword(Resource):
    @auth_user
    @is_role(['student', 'tutor'])
    @expect(change_password_parser)
    def post(self, current_user, data):
        user_service.change_password(current_user, data['password'])
        return {
            'msg': 'Password has been changed successfully'
            }

class GeneratePassword(Resource):
    @auth_user
    @is_role('admin')
    def get(self, current_user, username):
        new_password = user_service.generate_password(username)
        return {
            'password': new_password
            }