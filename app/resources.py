from flask_restful import Resource
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from app.parsers import *
from app.services import tutor_service, student_service, user_service, token_service
from app.exceptions import BaseException, InternalError
from flask import request

class TutorRegistration(Resource):
    def post(self):
        data = tutor_info_parser.parse_args()
        try:
            tutor_service.create_tutor(data)
            access_token = token_service.create_access_token(identity=data['username'])
            refresh_token = token_service.create_refresh_token(identity=data['username'])
            return {
                'msg': 'Tutor {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class TutorHome(Resource):
    @jwt_required
    def post(self):
        data = association_parser.parse_args()
        current_user = get_jwt_identity()
        try:
            tutor_service.add_association(current_user, **data)
            return {
                'msg': 'Association successfully created'
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        try:
            associations = tutor_service.get_associations(current_user)
            return associations
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class Checkpoints(Resource):
    @jwt_required
    def get(self, subject, group_id):
        current_user = get_jwt_identity()
        try:
            checkpoints = tutor_service.get_checkpoints(current_user, subject, group_id)
            return checkpoints
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

    @jwt_required
    def post(self, subject, group_id):
        #TODO допилить парсер
        data = request.get_json()
        current_user = get_jwt_identity()
        try:
            tutor_service.add_checkpoints(current_user, subject, group_id, data)
            return {
                'msg': 'Checkpoints succesfully created'
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class GroupCpProgress(Resource):
    @jwt_required
    def get(self, subject, group_id, cp_name):
        current_user = get_jwt_identity()
        try:
            progress = tutor_service.get_group_cp_progress(current_user, subject, group_id, cp_name)
            return progress
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

    @jwt_required
    def post(self, subject, group_id, cp_name):
        #TODO допилить парсер
        data = request.get_json()
        current_user = get_jwt_identity()
        try:
            tutor_service.add_group_cp_progress(current_user, subject, group_id, cp_name, data)
            return {
                'msg': 'Info succesfully updated'
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class StudentRegistration(Resource):
    def post(self):
        data = student_info_parser.parse_args()
        try:
            student_service.create_student(data)
            access_token = token_service.create_access_token(identity=data['username'])
            refresh_token = token_service.create_refresh_token(identity=data['username'])
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
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        try:
            subjects = student_service.get_subjects(current_user)
            return subjects
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class SubjectProgress(Resource):
    @jwt_required
    def get(self, subject):
        current_user = get_jwt_identity()
        try:
            progress = student_service.get_subject_progress(current_user, subject)
            return progress
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()


class UserLogin(Resource):
    def post(self):
        data = user_login_parser.parse_args()
        try:
            user_service.authenticate(data['username'], data['password'])
            access_token = token_service.create_access_token(identity=data['username'])
            refresh_token = token_service.create_refresh_token(identity=data['username'])
            return {
                'msg': 'Logged in as {}'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()
            
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            token_service.revoke_token(jti)
            return {'msg': 'Access token has been revoked'}
        except Exception as e:
            print(e)
            return InternalError().to_json()

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            token_service.revoke_token(jti)
            return {'msg': 'Refresh token has been revoked'}
        except Exception as e:
            print(e)
            return InternalError().to_json()

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = token_service.create_access_token(identity=current_user)
        return {'access_token': access_token}