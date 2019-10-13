from flask_restful import Resource
from app.parsers import tutor_reg_parser, student_reg_parser
from app.decorators import expect
from app.exceptions import BaseException, InternalError
from app.modules.tutor import TutorService
from app.modules.student import StudentService

student_service = StudentService()
tutor_service = TutorService()

class UserRegistration(Resource):
    @expect([tutor_reg_parser, student_reg_parser])
    def post(self, data):
        if data['role'] == 'tutor':
            tutor_service.create_tutor(data)