from flask_restful import Resource
from app.exceptions import BaseException, InternalError
from app.decorators import auth_user, is_role
from flask import request
from .checkpoint_service import CheckpointService

checkpoint_service = CheckpointService()

class Checkpoints(Resource):
    @auth_user
    def get(self, current_user, subject, group_id):
        try:
            checkpoints = tutor_service.get_checkpoints(current_user, subject, group_id)
            return checkpoints
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

    @auth_user
    @is_role(['admin', 'tutor'])
    def post(self, current_user, subject):
        #TODO допилить парсер
        data = request.get_json()
        try:
            return checkpoint_service.add(subject, data)
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

    @auth_user
    @is_role(['admin', 'tutor'])
    def delete(self, current_user, subject):
        #TODO допилить парсер
        data = request.get_json()
        try:
            checkpoint_service.delete(subject, data)
            return {'msg': 'Checkpoints has been succesfully deleted'}
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()