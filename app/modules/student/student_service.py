from app.models import User, Tutor, Student, Group, Subject, AssociationTGS, Checkpoint, CheckpointField, Progress
from app.modules.user import UserService
from app.utils import generate_password
from app import db
from app.exceptions import UserNotExist, AssociationNotExist
import datetime

user_service = UserService()

class StudentService:
    def _generate_group_id(self, group_number, admission_year):
        today = datetime.datetime.today()
        if today.year < admission_year:
            raise Exception('Wrong admission year')
        if today.month >= 9:
            sub = today.year - admission_year + 1
        else:
            sub = today.year - admission_year
        return int('73{}{}'.format(sub, group_number))

    def add_base_info(self, student: dict):
        admission_year, group_number = student['fullname'].split('-')[:2:] 
        admission_year = int(admission_year)
        password = generate_password() 
        group_id = self._generate_group_id(group_number, admission_year)
        student.update({
            'password': password,
            'admission_year': admission_year,
            'group_id': group_id
        })

    def create(self, data):
        self.add_base_info(data)
        user = user_service.create_user(data['username'], data['password'])
        group = Group.find_by_id(data['group_id'])
        if group is None:
            group = Group(id=data['group_id'])
            group.add_to_db()
        student = Student(fio=data['fio'],
                            fullname=data['fullname'],
                            admission_year=data['admission_year'], 
                            group_id=group.id)
        student.account = user
        student.add_to_db()
        db.session.commit()
        return data

    def find_student_by_username(self, username):
        user = user_service.find_by_username(username)
        if user is None:
            raise UserNotExist(username)
        return user.student

    def get_all(self):
        res = db.session.query(Student.fio, Student.fullname, Student.group_id, Student.admission_year, User.username).join(User).all()
        res = [{"username": x[4], "fullname": x[1], "fio": x[0], "group_id": x[2], "admission_year": x[3]} for x in res]
        return res

    def get_home_info(self, username):
        student = self.find_student_by_username(username)
        subjects = student.group.tgs.with_entities(AssociationTGS.subject_name).all()
        return [s[0] for s in subjects]

    def get_subjects(self, username):
        student = self.find_student_by_username(username)
        group = student.group
        tgs = group.tgs.distinct(AssociationTGS.tutor_id).all()
        tmp = { el.tutor_id: [] for el in tgs }
        tutors = [Tutor.json(Tutor.query.get(el.tutor_id), ['user_id']) for el in tgs]
        pairs = group.tgs.with_entities(AssociationTGS.tutor_id, AssociationTGS.subject_name).all()
        for pair in pairs:
            tmp[pair[0]].append(pair[1])
        index = 0
        for key in tmp:
            tutors[index]["subjects"] = tmp[key]
            index += 1
        return tutors
            