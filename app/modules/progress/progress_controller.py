from flask_restful import Resource
from app.decorators import auth_user, is_role
from flask import request
from .progress_service import ProgressService

progress_service = ProgressService()

class ProgressController(Resource):
    @auth_user
    @is_role('tutor')
    def post(self, current_user, subject, group_id):
        data = request.get_json()
        progress_service.add(current_user, subject, group_id, data)
        return {'msg': 'Result has been successfully added'}
    
    @auth_user
    @is_role(['tutor', 'student'])
    def get(self, current_user, subject, group_id):
        progress_service.get(current_user, subject, group_id)