from app import db
from app.models import User, Tutor, Student, Group, Subject, AssociationTGS, Checkpoint, Progress, CheckpointField, GroupInfo, DatesInfo
from app.modules.user import UserService
from app.modules.checkpoint import CheckpointService
from app.exceptions import UserNotExist, AssociationExist, AssociationNotExist, CheckpointNotExist, CheckpointExist, CheckpointFieldNotExist
from app.utils import generate_password

user_service = UserService()
checkpoint_service = CheckpointService()

class TutorService:
    def add_base_info(self, tutor):
        password = generate_password()
        tutor['password'] = password

    def create(self, data):
        self.add_base_info(data)
        user = user_service.create_user(data['username'], data['password'], role='tutor')
        tutor = Tutor(fio=data['fio'])
        tutor.account = user
        tutor.add_to_db()
        db.session.commit()
        return data
    
    def get_all(self):
        res = db.session.query(Tutor.fio, User.username).join(User).all()
        res = [{"username": x[1], "fio": x[0]} for x in res]
        return res

    def get_home_info(self, current_user):
        associations = self.get_associations(current_user)
        return associations

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

    def add_dates(self, username, subject_name, group_id, dates):
        tutor = self.find_tutor_by_username(username)
        tgs = self.find_tgs(tutor, subject_name, group_id)
        group_info = tgs.group_info.first()
        if group_info is None:
            group_info = GroupInfo()
            group_info.tgs = tgs
            tgs.group_info.append(group_info)
        for cp_name in dates:
            for date in dates[cp_name]:
                field = checkpoint_service.find_field_by_name(subject_name, cp_name, date['name'])
                date_info = group_info.dates.filter_by(group_info_id=group_info.id, date_field_id=field.id).first()
                if date_info is None:
                    date_info = DatesInfo()
                    date_info.group_info = group_info
                    date_info.checkpoint_field = field
                    field.dates_info.append(date_info)
                    group_info.dates.append(date_info)
                date_info.date = date['date']
        db.session.commit()