from flask_restful import Resource
from app.decorators import auth_user, is_role
from flask import request
from .checkpoint_service import CheckpointService

checkpoint_service = CheckpointService()

class Checkpoints(Resource):
    @auth_user
    @is_role(['admin', 'tutor'])
    def get(self, current_user, subject):
        checkpoints = checkpoint_service.get_all(subject)
        return checkpoints

    @auth_user
    @is_role(['admin', 'tutor'])
    def post(self, current_user, subject):
        #TODO допилить парсер
        data = request.get_json()
        return checkpoint_service.add(subject, data)

    @auth_user
    @is_role(['admin', 'tutor'])
    def delete(self, current_user, subject):
        #TODO допилить парсер
        data = request.get_json()
        checkpoint_service.delete(subject, data)
        return {'msg': 'Checkpoints has been succesfully deleted'}