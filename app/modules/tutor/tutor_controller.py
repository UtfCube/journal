from flask_restful import Resource
from app.decorators import auth_user, expect
from app.parsers import tutor_reg_parser, association_parser
from app.modules.auth import AuthService
from .tutor_service import TutorService
from app.exceptions import BaseException, InternalError

tutor_service = TutorService()
auth_service = AuthService()

class TutorRegistration(Resource):

    @expect(tutor_reg_parser)
    def post(self, data):
        try:
            tutor_service.create_tutor(data)
            access_token = auth_service.create_access_token(identity=data['username'])
            refresh_token = auth_service.create_refresh_token(identity=data['username'])
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
    @auth_user
    @expect(association_parser)
    def post(self, current_user, data):
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

    @auth_user
    def get(self, current_user):
        try:
            associations = tutor_service.get_associations(current_user)
            return associations
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()