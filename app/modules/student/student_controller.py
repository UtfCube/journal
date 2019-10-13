from flask_restful import Resource
from app.modules.auth import AuthService
from .student_service import StudentService
from app.parsers import student_reg_parser
from app.decorators import auth_user, expect
from app.exceptions import BaseException, InternalError

auth_service = AuthService()
student_service = StudentService()

class StudentRegistration(Resource):
    @expect(student_reg_parser)
    def post(self, data):
        try:
            student_service.create_student(data)
            access_token = auth_service.create_access_token(identity=data['username'])
            refresh_token = auth_service.create_refresh_token(identity=data['username'])
            return {
                'msg': 'Student {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

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