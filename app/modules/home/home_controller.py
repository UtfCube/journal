from flask_restful import Resource
from app.decorators import auth_user, is_role
from flask import request
from app import app
from app.modules.admin import AdminService
import csv
from .home_service import HomeService
from app.utils import save_file

admin_service = AdminService()
home_service = HomeService()

class HomeController(Resource):
    @auth_user
    @is_role('admin')
    def post(self, current_user):
        files = request.files
        results = {}
        if 'students' in files:
            students = files['students']
            path = save_file(app.config['ADMIN_FOLDER'], students)
            with open(path, 'r') as f:
                reader = csv.reader(f, delimiter=';')
                res = admin_service.create_students(list(reader)[1::])
                results['students'] = res
        if 'tutors' in files:
            tutors = files['tutors']
            path = save_file(app.config['ADMIN_FOLDER'], tutors)
            with open(path, 'r') as f:
                reader = csv.reader(f, delimiter=';')
                res = admin_service.create_tutors(list(reader)[1::])
                results['tutors'] = res
        subjects = [x for x in files if 'subject' in x]
        for subject in subjects:
            subject_file = files[subject]
            path = save_file(app.config['ADMIN_FOLDER'], subject_file)
            with open(path, 'r') as f:
                reader = list(csv.reader(f, delimiter=';'))
                subject_name = reader[0]
                checkpoints_list = reader[1::]
                res = admin_service.create_subject(subject_name, checkpoints_list)
                results[subject] = res
        return results
    
    @auth_user
    @is_role(['admin', 'tutor', 'student'])
    def get(self, current_user):
        return home_service.get(current_user)