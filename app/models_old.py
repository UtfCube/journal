from app import db, login
import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    """Info from db for flask-login"""
    return User.query.get(int(id))

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        """Define a base way to print models"""
        return "{}({})".format(self.__class__.__name__, {
                column: value
                for column, value in self._to_dict().items()
            })

    def json(self):
        """Define a base way to jsonify models, dealing with datetime objects"""
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

class User(UserMixin, BaseModel):
    """Model for the users table"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    tutor = db.relationship('Tutor', backref='account', uselist=False, lazy=True)
    student = db.relationship('Student', backref='account', uselist=False, lazy=True)

    def set_password(self, password):
        """Set User password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check User password"""
        return check_password_hash(self.password_hash, password)

class Person(BaseModel):
    """Model for the persons"""
    __abstract__ = True

    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    patronymic = db.Column(db.String(40), nullable=False)
    rank = db.Column(db.String(20), nullable=False) 

subjects_tutors = db.Table('subjects_tutors',
    db.Column('tutor_id', db.Integer, db.ForeignKey('tutors.user_id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)   
)

subjects_groups = db.Table('subjects_groups',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)   
)

class Tutor(Person):
    """Model for the tutors table"""
    __tablename__ = "tutors"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=False, nullable=False)
    degree = db.Column(db.String(10))
    subjects = db.relationship('Subject', secondary=subjects_tutors, lazy='dynamic',
        backref=db.backref('tutors', lazy='dynamic'))

class Group(BaseModel):
    """Model for the groups table"""
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    students = db.relationship('Student', backref='group', lazy='dynamic')
    subjects = db.relationship('Subject', secondary=subjects_groups, lazy='dynamic',
        backref=db.backref('groups', lazy='dynamic'))

class Subject(BaseModel):
    """Model for the subjects table"""
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    progress = db.relationship('Progress', backref=db.backref('subject'))

class Student(Person):
    """Model for the students table"""
    __tablename__ = "students"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=False, nullable=False)
    #record_book = db.Column(db.String(7), nullable=False)
    admission_year = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    progress = db.relationship('Progress', backref=db.backref('student'))

class Progress(BaseModel):
    """Model for the marks table"""
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.user_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    mark = db.Column(db.Integer, db.CheckConstraint('mark <= 5')) 

