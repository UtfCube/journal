from app.modules.tutor import TutorService
from app.modules.student import StudentService
import secrets
import string
import datetime
from app import db
from app.models import User, Tutor, Student, Group, Subject, AssociationTGS, Checkpoint, Progress, CheckpointField

student_service = StudentService()
tutor_service = TutorService()

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
        for checkpoint_info in checkpoints_list:
            fields = checkpoint_info[1::]
            field_count = len(fields)
            checkpoint_name = checkpoint_info[0]
            checkpoint = subject.checkpoints.filter_by(name=checkpoint_name).first()
            if checkpoint is None:
                checkpoint = Checkpoint(name=checkpoint_name)
                subject.checkpoints.append(checkpoint)
            mark = checkpoint.fields.filter_by(name='Оценка').first()
            if mark is None:
                mark = CheckpointField(name='Оценка', type='5')
                checkpoint.fields.append(mark)
            class_date = checkpoint.fields.filter_by(name='Дата проведения').first()
            if class_date is None:
                class_date = CheckpointField(name='Дата проведения')
                checkpoint.fields.append(class_date)
            if field_count > 0:
                for field_name in fields:
                    clean_field_name = field_name.replace('*', '').replace('+', '').replace('5', '')    
                    field = checkpoint.fields.filter_by(name=clean_field_name).first()
                    if field is None:
                        field = CheckpointField(name=clean_field_name)
                        checkpoint.fields.append(field)
                    if field_name.startswith('*'):
                        field.is_hidden = True
                    if field_name.endswith('+'):
                        field.type = '+'
                    elif field_name.endswith('5'):
                        field.type = '5'
                    else:
                        field.type = None
                if field_count > 1:
                    number_of_attempts = checkpoint.fields.filter_by(name='Число попыток сдачи').first()
                    if number_of_attempts is None:
                        number_of_attempts = CheckpointField(name='Число попыток сдачи')
                        checkpoint.fields.append(number_of_attempts)
                    completion_date = checkpoint.fields.filter_by(name='Дата сдачи').first()
                    if completion_date is None:
                        completion_date = CheckpointField(name='Дата сдачи')
                        checkpoint.fields.append(completion_date)
                    grace_period = checkpoint.fields.filter_by(name='Льготный срок сдачи').first()
                    if grace_period is None:
                        grace_period = CheckpointField(name='Льготный срок сдачи')
                        checkpoint.fields.append(grace_period)
                    deadline = checkpoint.fields.filter_by(name='Крайний срок сдачи').first()
                    if deadline is None:
                        deadline = CheckpointField(name='Крайний срок сдачи')
                        checkpoint.fields.append(deadline)
        db.session.commit()
        checkpoints = subject.checkpoints.all()
        return Checkpoint.json_list(checkpoints)