from app import db
from app.modules.student import StudentService
from app.modules.tutor import TutorService
from app.modules.user import UserService
from app.models import Progress, AssociationTGS, Student, Checkpoint, CheckpointField, User
from app.exceptions import SubjectNotExist, CheckpointNotExist, CheckpointFieldNotExist, AssociationNotExist
from operator import itemgetter
from itertools import groupby
from sqlalchemy import or_

user_service = UserService()
student_service = StudentService()
tutor_service = TutorService()


class ProgressService:
    def add(self, current_user, subject_name, group_id, data):
        tutor = tutor_service.find_tutor_by_username(current_user)
        tgs = tutor_service.find_tgs(tutor, subject_name, group_id)
        for result in data:
            student = student_service.find_student_by_username(result['username'])
            progress = result['progress']
            for p in progress:
                checkpoint_name = p['name']
                checkpoint = tgs.subject.checkpoints.filter_by(name=checkpoint_name).first()
                if checkpoint is None:
                    raise CheckpointNotExist(checkpoint_name)
                results = p['results']
                for result in results:
                    field_name = result['name']
                    field = checkpoint.fields.filter_by(name=field_name).first()
                    if field is None:
                        raise CheckpointFieldNotExist(checkpoint_name, field_name)
                    progress = field.progress.filter_by(student_id=student.user_id).first()
                    if progress is None:
                        progress = Progress()
                        progress.checkpoint_field = field
                        student.progress.append(progress)
                    progress.result = result['result']
        db.session.commit()

    def get(self, current_user, subject_name, group_id):
        user = user_service.find_by_username(current_user)
        if user.role == 'tutor':
            tutor = user.tutor
            tgs = tutor_service.find_tgs(tutor, subject_name, group_id)
        else:
            student = user.student
            group_id =student.group_id
            tgs = AssociationTGS.query.filter_by(subject_name=subject_name, group_id=group_id).first()
            if tgs is None:
                raise AssociationNotExist(subject_name=subject_name, group_id=group_id)
        subject = tgs.subject
        if subject is None: 
            raise SubjectNotExist(subject_name)
        res: list = (db.session.query(Student, User.username, Progress.result, CheckpointField.name, Checkpoint.name)
            .join(User)
            .outerjoin(Progress)
            .outerjoin(CheckpointField)
            .outerjoin(Checkpoint)
            .filter(or_(Checkpoint.subject_name==subject_name, Checkpoint.subject_name == None))
            .filter(Student.group_id==group_id)).all()
        res = {k: [(d,z,y) for a,x,y,z,d in g] for k,g in groupby(res, key=itemgetter(0, 1))}
        results = []
        for s in res:
            t = res[s]
            t.sort(key=itemgetter(0))
            results.append({"username": s[1], 
                **Student.json(s[0], ['user_id', 'admission_year', 'group_id']),
                "progress": [{"name": k, "results": [{"name": y, "result":z} for x,y,z in g] } for k,g in groupby(t, key=itemgetter(0)) if k is not None]})
        print(results)
        return results