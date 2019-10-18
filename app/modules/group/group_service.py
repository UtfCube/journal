from app.models import Group

class GroupService:
    def get_all(self):
        groups = Group.query.all()
        return Group.json_list(groups)