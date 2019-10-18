from app.models import Subject

class SubjectService:
    def get_all(self):
        subjects = Subject.query.all()
        return Subject.json_list(subjects)