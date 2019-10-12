from flask_restful import Resource
from app.exceptions import BaseException, InternalError
from app.decorators import auth_user
from flask import request

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
    def post(self, current_user, subject, group_id):
        #TODO допилить парсер
        data = request.get_json()
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