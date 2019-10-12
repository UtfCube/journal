from flask_restful import Resource
from app.decorators import auth_user, is_admin
from flask import request
from app import app
from .admin_service import AdminService
import os
import csv
from werkzeug.utils import secure_filename

admin_service = AdminService()

def save_file(folder, file):
    filename = secure_filename(file.filename)
    path = os.path.join(folder, filename)
    file.save(path)
    return path

class AdminHome(Resource):
    @auth_user
    @is_admin
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
        return {
            'msg': 'success', 
            'res': results
        }