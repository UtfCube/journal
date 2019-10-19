from app import db
from app.modules.student import StudentService
from app.modules.tutor import TutorService
from app.modules.user import UserService
from app.models import Progress, AssociationTGS, Student, Checkpoint, CheckpointField
from app.exceptions import SubjectNotExist, CheckpointNotExist, CheckpointFieldNotExist, AssociationNotExist
from operator import itemgetter
from itertools import groupby

user_service = UserService()
student_service = StudentService()
tutor_service = TutorService()


class ProgressService:
    def add(self, current_user, subject_name, group_id, data):
        tutor = tutor_service.find_tutor_by_username(current_user)
        tgs = tutor_service.find_tgs(tutor, subject_name, group_id)
        for result in data:
            student = student_service.find_student_by_username(result['student_username'])
            checkpoint_name = result['checkpoint']
            checkpoint = tgs.subject.checkpoints.filter_by(name=checkpoint_name).first()
            if checkpoint is None:
                raise CheckpointNotExist(checkpoint_name)
            field_name = result['field']
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
            tgs = AssociationTGS.query.filter_by(subject_name=subject_name, group_id=group_id).first()
            if tgs is None:
                raise AssociationNotExist(subject_name=subject_name, group_id=group_id)
        group = tgs.group
        students = group.students.all()
        progress = Student.json_list(students)
        subject = tgs.subject
        if subject is None: 
            raise SubjectNotExist(subject_name)
        #for 
        res: list = (db.session.query(Checkpoint.name, CheckpointField.name, Progress.result, Student)
            .join(CheckpointField)
            .join(Progress)
            .join(Student)
            .filter(Checkpoint.subject_name==subject_name)
            .filter(Student.group_id==group_id)).all()
        #print(res)
        #res.sort(key=lambda x: x[3].user_id)
        res = {k: [(x,y,z) for x,y,z,d in g] for k,g in groupby(res, key=itemgetter(3))}
        #print(res)
        for s in res:
            t = res[s]
            t.sort(key=itemgetter(0))
            res[s] = {k: [(y,z) for x,y,z in g] for k,g in groupby(t, key=itemgetter(0))}
        print(res)
        #res.sort(key=itemgetter(0, 3))
        #
        #print({str(k):[(y,z) for x,y,z,d in v] for k,v in groupby(res, key=itemgetter(0, 3))})
        #checkpoints = subject.checkpoints.all()
        #for checkpoint in checkpoints:

        #for i, student in enumerate(students):
        #    pass