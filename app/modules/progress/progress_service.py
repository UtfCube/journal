from app import db
from app.modules.student import StudentService
from app.modules.tutor import TutorService
from app.models import Progress
from app.exceptions import SubjectNotExist, CheckpointNotExist, CheckpointFieldNotExist

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
