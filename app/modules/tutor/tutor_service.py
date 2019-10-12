from app import db
from app.models import User, Tutor, Student, Group, Subject, AssociationTGS, Checkpoint, Progress, CheckpointField
from app.modules.user import UserService
from app.exceptions import UserNotExist, AssociationExist, AssociationNotExist, CheckpointNotExist, CheckpointExist, CheckpointFieldNotExist

user_service = UserService()

class TutorService:
    def create_tutor(self, data):
        user = user_service.create_user(data['username'], data['password'])
        tutor = Tutor(fio=data['fio'])
        tutor.account = user
        tutor.add_to_db()
        db.session.commit()
        return tutor
    
    def find_tutor_by_username(self, username):
        user = user_service.find_by_username(username)
        if user is None:
            raise UserNotExist(username)
        return user.tutor
    
    def find_tgs(self, tutor, subject_name, group_id):
        tgs = tutor.tgs.filter_by(subject_name=subject_name, group_id=group_id).first()
        if tgs is None:
            raise AssociationNotExist(subject_name=subject_name, group_id=group_id)
        return tgs

    def find_checkpoint_by_name(self, tgs, name):
        checkpoint = tgs.checkpoints.filter_by(name=name).first()
        if Checkpoint is None:
            raise CheckpointNotExist(name)
        return checkpoint 

    def get_associations(self, username):
        tutor = self.find_tutor_by_username(username)
        associations = tutor.tgs.all()
        return AssociationTGS.json_list(associations, ['id', 'tutor_id'])

    def add_association(self, username, subject_name, group_id):
        tutor = self.find_tutor_by_username(username)
        if tutor.tgs.filter_by(subject_name=subject_name, group_id=group_id).first():
            raise AssociationExist(subject_name=subject_name, group_id=group_id)
        subject = Subject.find_by_name(subject_name)
        if subject is None:
            subject = Subject(name=subject_name)
            subject.add_to_db()
        group = Group.find_by_id(group_id)
        if group is None: 
            group = Group(id=group_id)
            group.add_to_db()
        association = AssociationTGS()
        association.subject = subject
        association.group = group
        tutor.tgs.append(association)
        db.session.commit()

    def get_checkpoints(self, username, subject_name, group_id):
        tutor = self.find_tutor_by_username(username)
        tgs = self.find_tgs(tutor, subject_name, group_id)
        res = {}
        checkpoints = tgs.checkpoints.all()
        res['checkpoints'] = Checkpoint.json_list(checkpoints, ['id', 'tgs_id'])
        for i, checkpoint in enumerate(checkpoints):
            #res['checkpoints'][i]['fields'] = Checkpoint.json_list(checkpoint.fields, ['id', 'checkpoint_id'])
            res['checkpoints'][i]['fields'] = [ field.name for field in checkpoint.fields ]
        return res

    def add_checkpoints(self, username, subject_name, group_id, data):
        tutor = self.find_tutor_by_username(username)
        tgs = self.find_tgs(tutor, subject_name, group_id)
        group = tgs.group
        checkpoints = data['checkpoints']
        for cp_json in checkpoints:
            cp_name = cp_json['name']
            if tgs.checkpoints.filter_by(name=cp_name).first():
                raise CheckpointExist(cp_name)
            checkpoint = Checkpoint(name=cp_name, tgs_id=tgs.id)
            db.session.add(checkpoint)
            for cp_field_json in cp_json['fields']:
                cp_field = CheckpointField(name=cp_field_json, checkpoint_id=checkpoint.id)
                checkpoint.fields.append(cp_field)
            for student in group.students:
                for cp_field in checkpoint.fields:
                    progress = Progress(checkpoint_field_id=cp_field.id,
                                        student_id=student.user_id)
                    student.progress.append(progress)
        db.session.commit()

    def get_group_cp_progress(self, username, subject_name, group_id, cp_name):
        tutor = self.find_tutor_by_username(username)
        tgs = self.find_tgs(tutor, subject_name, group_id)
        group = tgs.group
        checkpoint = self.find_checkpoint_by_name(tgs, cp_name)
        students = group.students.all()
        progress = Student.json_list(students)
        for i, student in enumerate(students):
            cp_progress = (db.session.query(CheckpointField.name,
                                Progress.passed)
                            .join(Progress)
                            .filter(CheckpointField.checkpoint_id == checkpoint.id)
                            .filter(Progress.student_id == student.user_id)
                            ).all()
            progress[i]['progress'] = dict(cp_progress)
        return progress
    
    def add_group_cp_progress(self, username, subject_name, group_id, cp_name, data):
        tutor = self.find_tutor_by_username(username)
        tgs = self.find_tgs(tutor, subject_name, group_id)
        checkpoint = self.find_checkpoint_by_name(tgs, cp_name)
        for user_info in data:
            student = tgs.group.students.filter_by(user_id=user_info['user_id']).first()
            if student is None:
                raise UserNotExist(user_info['user_id'])
            for field_name, field_value in user_info['progress'].items():
                progress_id = (db.session.query(CheckpointField.id)
                            .join(Progress)
                            .filter(CheckpointField.checkpoint_id == checkpoint.id)
                            .filter(Progress.student_id == student.user_id)
                            .filter(CheckpointField.name == field_name)
                            ).first()
                if progress_id is None:
                    raise CheckpointFieldNotExist(cp_name, field_name)
                progress_id = progress_id[0] 
                Progress.query.filter_by(checkpoint_field_id=progress_id, student_id=student.user_id).update({"passed": field_value})
        db.session.commit()