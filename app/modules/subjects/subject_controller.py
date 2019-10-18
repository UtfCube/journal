from app.decorators import auth_user, is_role
from flask_restful import Resource
from .subject_service import SubjectService

subject_service = SubjectService()

class SubjectController(Resource):
    @auth_user
    @is_role(['tutor', 'student'])
    def get(self, current_user):
        subjects = subject_service.get_all()
        return subjects
