from app.modules.tutor import TutorService
from app.modules.student import StudentService
from app.modules.checkpoint import CheckpointService
from app import db

student_service = StudentService()
tutor_service = TutorService()
checkpoint_service = CheckpointService()

class AdminService:
    def create_students(self, students_list):
        results = []
        for student_info in students_list:
            fullname = student_info[1]
            fio = student_info[0]
            login = student_info[2]
            student = {
                'fullname': fullname,
                'username': login,
                'fio': fio,
            }
            student = student_service.create(student)
            results.append(student)
        return results

    def create_tutors(self, tutors_list):
        results = []
        for tutor_info in tutors_list:
            fio = tutor_info[0]
            login = tutor_info[1]
            tutor = {
                'username': login,
                'fio': fio
            }
            tutor = tutor_service.create(tutor)
            results.append(tutor)
        return results

    def create_subject(self, subject_name, checkpoints):
        subject_name = subject_name[0]
        checkpoints = checkpoint_service.from_csv(checkpoints)
        return checkpoint_service.add(subject_name, checkpoints)