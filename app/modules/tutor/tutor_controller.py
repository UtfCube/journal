from flask_restful import Resource
from app.decorators import auth_user, expect, is_role
from app.parsers import tutor_reg_parser, association_parser
from app.modules.auth import AuthService
from .tutor_service import TutorService
from flask import request

tutor_service = TutorService()
auth_service = AuthService()

class Tutors(Resource):
    @auth_user
    def get(self, current_user):
        return tutor_service.get_all()

class GroupSubject(Resource):
    @auth_user
    @is_role('tutor')
    @expect(association_parser)
    def post(self, current_user, data):
        tutor_service.add_association(current_user, **data)
        return {
            'msg': 'Association successfully created'
        }
    
    @auth_user
    @is_role('tutor')
    def get(self, current_user):
        associations = tutor_service.get_associations(current_user)
        return associations

class Dates(Resource):
    @auth_user
    @is_role('tutor')
    def post(self, current_user, subject, group_id):
        #TODO допилить парсер
        data = request.get_json()
        tutor_service.add_dates(current_user, subject, group_id, data)
        return {
            'msg': 'Dates successfully created/updated'
        }