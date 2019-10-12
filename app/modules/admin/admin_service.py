from app.modules.tutor import TutorService
from app.modules.student import StudentService
from app.modules.checkpoint import CheckpointService
import secrets
import string
import datetime
from app import db
from app.models import User, Tutor, Student, Group, Subject, AssociationTGS, Checkpoint, Progress, CheckpointField

student_service = StudentService()
tutor_service = TutorService()
checkpoint_service = CheckpointService()

class AdminService:
    def _generate_password(self):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(8))
    
    def _generate_group_id(self, group_number, admission_year):
        today = datetime.datetime.today()
        if today.year < admission_year:
            raise Exception('Wrong admission year')
        if today.month >= 9:
            sub = today.year - admission_year + 1
        else:
            sub = today.year - admission_year
        return int('73{}{}'.format(sub, group_number))

    def create_students(self, students_list):
        results = []
        for student_info in students_list:
            fullname = student_info[1]
            admission_year, group_number = fullname.split('-')[:2:] 
            admission_year = int(admission_year)
            fio = student_info[0]
            login = student_info[2]
            password = self._generate_password() 
            group_id = self._generate_group_id(group_number, admission_year)
            res = {
                'fullname': fullname,
                'username': login,
                'password': password
            }
            student_db_data = {
                **res,
                'fio': fio,
                'admission_year': admission_year,
                'group_id': group_id
            }
            student_service.create_student(student_db_data)
            results.append(res)
        return results

    def create_tutors(self, tutors_list):
        results = []
        for tutor_info in tutors_list:
            fio = tutor_info[0]
            login = tutor_info[1]
            password = self._generate_password() 
            res = {
                'username': login,
                'password': password
            }
            tutor_db_data = {
                **res,
                'fio': fio
            }
            tutor_service.create_tutor(tutor_db_data)
            results.append(res)
        return results

    def create_subject(self, subject_name, checkpoints_list):
        subject_name = subject_name[0]
        subject = Subject.query.filter_by(name=subject_name).first()
        if subject is None: 
            subject = Subject(name=subject_name)
            subject.add_to_db()
        checkpoints_json = checkpoint_service.from_csv(checkpoints_list)
        checkpoints = subject.checkpoints
        for checkpoint_json in checkpoints_json:
            checkpoint_name =  checkpoint_json['name']
            checkpoint = checkpoints.filter_by(name=checkpoint_name).first()
            if checkpoint is None:
                checkpoint = Checkpoint(name=checkpoint_name)
                checkpoints.append(checkpoint)
            fields = checkpoint.fields
            for field_json in checkpoint_json['fields']:
                field_name = field_json['name']
                field = fields.filter_by(name=field_name).first()
                if field is None:
                    field = CheckpointField(name=field_name)
                    fields.append(field)
                field.type = field_json.get('type', None)
                field.is_hidden = field_json.get('is_hidden', False)
        db.session.commit()
        checkpoints = subject.checkpoints.all()
        return Checkpoint.json_list(checkpoints)