from app.decorators import auth_user, is_role
from flask_restful import Resource
from .group_service import GroupService

group_service = GroupService()

class GroupController(Resource):
    @auth_user
    @is_role(['tutor'])
    def get(self, current_user):
        groups = group_service.get_all()
        return groups
