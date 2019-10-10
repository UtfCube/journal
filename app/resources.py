from flask_restful import Resource
from app.parsers import *
from app.services import tutor_service, student_service, user_service, token_service, admin_service
from app.exceptions import BaseException, InternalError
from app.modules import AuthUser, is_admin
from flask import request
from werkzeug.utils import secure_filename
from app import app
import os
import csv

class TutorRegistration(Resource):
    def post(self):
        data = tutor_info_parser.parse_args()
        try:
            tutor_service.create_tutor(data)
            access_token = token_service.create_access_token(identity=data['username'])
            refresh_token = token_service.create_refresh_token(identity=data['username'])
            return {
                'msg': 'Tutor {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class TutorHome(Resource):
    @AuthUser
    def post(self, current_user):
        data = association_parser.parse_args()
        try:
            tutor_service.add_association(current_user, **data)
            return {
                'msg': 'Association successfully created'
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

    @AuthUser
    def get(self, current_user):
        try:
            associations = tutor_service.get_associations(current_user)
            return associations
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

def save_file(folder, file):
    filename = secure_filename(file.filename)
    path = os.path.join(folder, filename)
    file.save(path)
    return path

class AdminHome(Resource):
    @AuthUser
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

class Checkpoints(Resource):
    @AuthUser
    def get(self, current_user, subject, group_id):
        try:
            checkpoints = tutor_service.get_checkpoints(current_user, subject, group_id)
            return checkpoints
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

    @AuthUser
    def post(self, current_user, subject, group_id):
        #TODO допилить парсер
        data = request.get_json()
        try:
            tutor_service.add_checkpoints(current_user, subject, group_id, data)
            return {
                'msg': 'Checkpoints succesfully created'
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class GroupCpProgress(Resource):
    @AuthUser
    def get(self, current_user, subject, group_id, cp_name):
        try:
            progress = tutor_service.get_group_cp_progress(current_user, subject, group_id, cp_name)
            return progress
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

    @AuthUser
    def post(self, current_user, subject, group_id, cp_name):
        #TODO допилить парсер
        data = request.get_json()
        try:
            tutor_service.add_group_cp_progress(current_user, subject, group_id, cp_name, data)
            return {
                'msg': 'Info succesfully updated'
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class StudentRegistration(Resource):
    def post(self):
        data = student_info_parser.parse_args()
        try:
            student_service.create_student(data)
            access_token = token_service.create_access_token(identity=data['username'])
            refresh_token = token_service.create_refresh_token(identity=data['username'])
            return {
                'msg': 'Student {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class StudentHome(Resource):
    @AuthUser
    def get(self, current_user):
        try:
            subjects = student_service.get_subjects(current_user)
            return subjects
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class SubjectProgress(Resource):
    @AuthUser
    def get(self, current_user, subject):
        try:
            progress = student_service.get_subject_progress(current_user, subject)
            return progress
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()