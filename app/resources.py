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