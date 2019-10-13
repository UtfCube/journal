from app.modules.tutor import TutorService
from app.modules.student import StudentService
from app.decorators import expect
from app.parsers import tutor_reg_parser, student_reg_parser
from app.exceptions import BaseException, InternalError
from flask_restful import Resource

student_service = StudentService()
tutor_service = TutorService()

class UserRegistration(Resource):
    @expect([student_reg_parser, tutor_reg_parser])
    def post(self, data):
        try:
            if data['role'] == 'tutor':
                user = tutor_service.create(data)
            else:
                user = student_service.create(data)
            return user
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()