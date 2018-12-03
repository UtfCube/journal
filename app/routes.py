# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, StudentRegistrationForm, TutorRegistrationForm, SubjectsEditForm
from app.models import User, Tutor, Student, Group, Subject, Progress, AssociationTGS
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.tutor is None:
        return redirect(url_for('student_home'))
    else:
        return redirect(url_for('tutor_home'))

@app.route('/tutor/home', methods=['GET', 'POST'])
@login_required
def tutor_home():
    form = SubjectsEditForm()
    tutor = current_user.tutor
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

@app.route('/student/home')
@login_required
def student_home():
    student = current_user.student
    subjects = [ x[0] for x in student.group.tgs.with_entities(AssociationTGS.subject_name)]
    print(subjects)
    return render_template('student_home.html', title='Home', subjects=subjects)

@app.route('/tutor/subjects/change')
@login_required
def change_subjects():
    return render_template('index.html', title='Настройка')

@app.route('/tutor/<subject>', methods=['GET', 'POST'])
@login_required
def change_subject_progress(subject):
    pass

@app.route('/student/<subject>')
@login_required
def get_subject_progress(subject):
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        #next if is for defence from xss
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register/<type>', methods=['GET', 'POST'])
def register(type):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if type == 'tutor':
        form = TutorRegistrationForm()
    else:
        form = StudentRegistrationForm()

    if form.validate_on_submit():
        #TODO: here is possible sql injection
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        if isinstance(form, TutorRegistrationForm):
            tutor = Tutor(user_id=user.id,
                            lastname=form.lastname.data,
                            firstname=form.firstname.data,
                            patronymic=form.patronymic.data,
                            rank=form.rank.data, 
                            degree=form.degree.data)
            db.session.add(tutor)
        else:
            group = Group.query.filter_by(id=form.group_id.data).first()
            if group is None:
                group = Group(id=form.group_id.data)
                db.session.add(group)
            student = Student(user_id=user.id,
                                lastname=form.lastname.data,
                                firstname=form.firstname.data,
                                patronymic=form.patronymic.data,
                                rank=form.rank.data, 
                                admission_year=form.admission_year.data, 
                                group_id=group.id)
            db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', type=type, form=form)