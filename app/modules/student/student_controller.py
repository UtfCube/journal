from flask_restful import Resource
from app.modules.auth import AuthService
from .student_service import StudentService
from app.parsers import student_reg_parser
from app.decorators import auth_user, expect

auth_service = AuthService()
student_service = StudentService()

class StudentHome(Resource):
    @auth_user
    def get(self, current_user):
        subjects = student_service.get_home_info(current_user)
        return subjects