from flask_restful import Resource
from app.decorators import auth_user, expect, is_role
from app.parsers import change_password_parser
from .user_service import UserService

user_service = UserService()

class ChangePassword(Resource):
    @auth_user
    @is_role(['student', 'tutor'])
    @expect(change_password_parser)
    def post(self, current_user, data):
        print(current_user)
        user_service.change_password(current_user, data['password'])
        return {
            'msg': 'Password has been changed successfully'
            }