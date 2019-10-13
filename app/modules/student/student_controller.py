from flask_restful import Resource
from app.modules.auth import AuthService
from .student_service import StudentService
from app.parsers import student_reg_parser
from app.decorators import auth_user, expect
from app.exceptions import BaseException, InternalError

auth_service = AuthService()
student_service = StudentService()

class StudentHome(Resource):
    @auth_user
    def get(self, current_user):
        try:
            subjects = student_service.get_subjects(current_user)
            return subjects
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()