from app.modules.tutor import TutorService
from app.modules.student import StudentService
from app.decorators import expect
from app.parsers import tutor_reg_parser, student_reg_parser
from flask_restful import Resource

student_service = StudentService()
tutor_service = TutorService()

class UserRegistration(Resource):
    @expect([student_reg_parser, tutor_reg_parser])
    def post(self, data):
        if data['role'] == 'tutor':
            user = tutor_service.create(data)
        else:
            user = student_service.create(data)
        return user