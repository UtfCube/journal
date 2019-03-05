from app import db
import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    '''
    def __repr__(self):
        """Define a base way to print models"""
        return "{}({})".format(self.__class__.__name__, {
                column: value
                for column, value in self._to_dict().items()
            })
    '''

    def json(self):
        """Define a base way to jsonify models, dealing with datetime objects"""
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

class User(BaseModel):
    """Model for the users table"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    tutor = db.relationship('Tutor', backref='account', uselist=False, lazy=True)
    student = db.relationship('Student', backref='account', uselist=False, lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return None

        return user

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

class AssociationTGS(BaseModel):
    """Model for the tgs table"""
    __tablename__ = "tgs"

    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.user_id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    subject_name = db.Column(db.String(128), db.ForeignKey('subjects.name'), primary_key=True)

class Tutor(Person):
    """Model for the tutors table"""
    __tablename__ = "tutors"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=False, nullable=False)
    degree = db.Column(db.String(10))
    tgs = db.relationship('AssociationTGS', lazy='dynamic',
        backref=db.backref('tutor', lazy=True), cascade='all,delete-orphan')
    checkpoints = db.relationship('Checkpoint', lazy='dynamic',
        backref=db.backref('tutor', lazy=True), cascade='all,delete-orphan') 

class Group(BaseModel):
    """Model for the groups table"""
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    students = db.relationship('Student', backref='group', lazy='dynamic')
    tgs = db.relationship('AssociationTGS', lazy='dynamic',
        backref=db.backref('group', lazy=True), cascade='all,delete-orphan')

class Subject(BaseModel):
    """Model for the subjects table"""
    __tablename__ = "subjects"

    name = db.Column(db.String(128), primary_key=True)
    #progress = db.relationship('Progress', backref=db.backref('subject'), lazy='dynamic', cascade='all,delete-orphan')
    tgs = db.relationship('AssociationTGS', lazy='dynamic',
        backref=db.backref('subject', lazy=True), cascade='all,delete-orphan') 
    checkpoints = db.relationship('Checkpoint', lazy='dynamic',
        backref=db.backref('subject', lazy=True), cascade='all,delete-orphan') 

class Student(Person):
    """Model for the students table"""
    __tablename__ = "students"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=False, nullable=False)
    admission_year = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    progress = db.relationship('Progress', backref=db.backref('student', lazy=True), lazy='dynamic', cascade='all,delete-orphan')

class Checkpoint(BaseModel):
    """Model for the checkpoints table"""
    __tablename__ = "checkpoints"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    posting_date = db.Column(db.DateTime, nullable=False)
    critical_date = db.Column(db.DateTime, nullable=False)
    subject_name = db.Column(db.String(128), db.ForeignKey('subjects.name'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutors.user_id"), nullable=False)
    progress = db.relationship('Progress', lazy='dynamic',
        backref=db.backref('checkpoint', lazy=True), cascade='all,delete-orphan') 

class Progress(BaseModel):
    """Model for the marks table"""
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.user_id'), nullable=False)
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoints.id'), nullable=False)
    pass_date = db.Column(db.DateTime)
    approaches_number = db.Column(db.Integer, default=0, nullable=False)
    #mark = db.Column(db.Integer, db.CheckConstraint('mark <= 5')) 

