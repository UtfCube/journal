# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, StudentRegistrationForm, TutorRegistrationForm, SubjectsEditForm, CheckPointForm
from functools import wraps  
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request, current_app

import jwt

from app.models import User, Tutor, Student, Group, Subject, Progress, AssociationTGS
from werkzeug.urls import url_parse
import requests
import json

def token_required(func):
    @wraps(func)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(username=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return func(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401   
    return _verify


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

def get_user_type(user):
    tutor = Tutor.query.filter_by(user_id=user.id).first()
    if not tutor:
        return 'student'
    else:
        return 'tutor'

@app.route('/api/login', methods=['POST'])
def login():
    print('login')
    if request.method == 'POST':
        data = request.get_json()
        if data:
            print(data)
            user = User.authenticate(**data)
            if not user:
                return jsonify({"message": "invalid credentials", "authenticated": False}), 401
            token = jwt.encode({
                'sub': user.username,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=30)},
                current_app.config['SECRET_KEY'])
            return jsonify({ 'token': token.decode('UTF-8'), 'type': get_user_type(user) })

@app.route('/api/register/<type>', methods=['POST'])
def register(type):
    if request.method == 'POST':
        data = request.get_json()
        if type == 'tutor':
            user = User(data['username'], data['password'])
            db.session.add(user)
            db.session.commit()
            tutor = Tutor(user_id=user.id,
                            lastname=data.get('lastname'),
                            firstname=data.get('firstname'),
                            patronymic=data.get('patronymic'),
                            rank=data.get('rank'), 
                            degree=data.get('degree'))
            db.session.add(tutor)
        elif type == 'student':
            user = User(data['username'], data['password'])
            db.session.add(user)
            db.session.commit()
            group = Group.query.filter_by(id=data.get('group_id')).first()
            if group is None:
                group = Group(id=data.get('group_id'))
                db.session.add(group)
            student = Student(user_id=user.id,
                                lastname=data.get('lastname'),
                                firstname=data.get('firstname'),
                                patronymic=data.get('patronymic'),
                                rank=data.get('rank'), 
                                admission_year=data.get('admission_year'), 
                                group_id=group.id)
            db.session.add(student)
        db.session.commit()
        db.session.remove()
        print('user_created')
        return jsonify({"message": "You are now a register user"}), 200

@app.route('/tutor/home', methods=['GET', 'POST'])
def tutor_home():
    form = SubjectsEditForm()
    tutor = {}
    if form.validate_on_submit():
        if form.add.data:
            subject = Subject.query.get(form.subject.data)
            if subject is None:
                subject = Subject(name=form.subject.data)
                db.session.add(subject)
            group = Group.query.get(form.group_id.data)
            if group is None:
                group = Group(id=form.group_id.data)
                db.session.add(group)
            association = AssociationTGS()
            association.subject = subject
            association.group = group
            tutor.tgs.append(association)
            db.session.commit()
        elif form.delete.data:
            association = tutor.tgs.filter_by(group_id=form.group_id.data, subject_name=form.subject.data).first()
            tutor.tgs.remove(association)
            db.session.commit()
    associations = tutor.tgs.all() 
    return render_template('tutor_home.html', title='Home', associations=associations, form=form)

@app.route('/api/student/home')
@token_required
def student_home(user):
    #student = current_user.student
    student = Student.query.filter_by(user_id=user.id).first()
    print(student.group_id)
    group = Group.query.filter_by(id=student.group_id).first()
    print(group)
    subjects = [x[0] for x in group.tgs.with_entities(AssociationTGS.subject_name)]
    return jsonify({"username": user.username, "subjects": subjects})
    #return render_template('student_home.html', title='Home', subjects=subjects)

@app.route('/tutor/subjects/change')
def change_subjects():
    return render_template('index.html', title='Настройка')

@app.route('/tutor/<subject>/<group_id>', methods=['GET', 'POST'])
def change_subject_progress(subject, group_id):
    form = CheckPointForm()
    group_progress = db.session.query(Student, Progress).join(Progress.student).\
                        filter(Student.group_id==group_id).\
                        filter(Progress.subject_name==subject)        
    checkpoints = db.session.query(Progress.checkpoint_name,
                                    Progress.posting_date,
                                    Progress.critical_date    
                                    ).join(Student.progress).\
                                        filter_by(subject_name=subject).\
                                        group_by(Progress.checkpoint_name,
                                                    Progress.posting_date,
                                                    Progress.critical_date).all()
    
    if form.validate_on_submit():
        checkpoint = group_progress.filter_by(checkpoint_name=form.name.data).first()
        if checkpoint is None:
            progress = Progress(checkpoint_name=form.name.data,
                            posting_date=form.posting_date.data,
                            critical_date=form.critical_date.data)
            subj = Subject.query.get(subject)
            progress.subject = subj
            group = Group.query.get(group_id)
            students = group.students
            #TODO переделать бд, чтобы менять поля в одной записи
            for student in students:
                student.progress.append(progress)
            db.session.commit()
    else:
        print("not valid")
    group_progress = group_progress.all()   
    return render_template('checkpoints.html', title='Контрольные точки', checkpoints=checkpoints, group_progress=group_progress, form=form)

"""
@app.route('/student/<subject>')
def get_subject_progress(subject):
    student = current_user.student
    student_progress = student.progress.filter_by(subject_name=subject).all()
    return render_template('progress.html', title='Успеваемость', student_progress=student_progress)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
"""