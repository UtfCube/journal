from app import db
import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash
from .serializer import Serializer 


def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d


class BaseModel(db.Model, Serializer):
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
        return to_json(self, self.__class__)

    @staticmethod
    def json_list(lst):
        return [i.json() for i in lst]

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
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.user_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    subject_name = db.Column(db.String(128), db.ForeignKey('subjects.name'), nullable=False)
    checkpoints = db.relationship('Checkpoint', lazy='dynamic',
        backref=db.backref('tgs', lazy=True), cascade='all,delete-orphan') 
    
    def serialize(self):
        return { "group_id": self.group_id,
                 "subject_name": self.subject_name }

class Tutor(Person):
    """Model for the tutors table"""
    __tablename__ = "tutors"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=False, nullable=False)
    degree = db.Column(db.String(10))
    tgs = db.relationship('AssociationTGS', lazy='dynamic',
        backref=db.backref('tutor', lazy=True), cascade='all,delete-orphan')
    # checkpoints = db.relationship('Checkpoint', lazy='dynamic',
    #    backref=db.backref('tutor', lazy=True), cascade='all,delete-orphan') 

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
    # checkpoints = db.relationship('Checkpoint', lazy='dynamic',
    #    backref=db.backref('subject', lazy=True), cascade='all,delete-orphan') 

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
    posting_date = db.Column(db.Date, nullable=False)
    critical_date = db.Column(db.Date, nullable=False)
    #subject_name = db.Column(db.String(128), db.ForeignKey('subjects.name'), nullable=False)
    #tutor_id = db.Column(db.Integer, db.ForeignKey("tutors.user_id"), nullable=False)
    progress = db.relationship('Progress', lazy='dynamic',
        backref=db.backref('checkpoint', lazy=True), cascade='all,delete-orphan') 
    tgs_id = db.Column(db.Integer, db.ForeignKey('tgs.id'), nullable=False)

class Progress(BaseModel):
    """Model for the marks table"""
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.user_id'), nullable=False)
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoints.id'), nullable=False)
    pass_date = db.Column(db.Date)
    approaches_number = db.Column(db.Integer, default=0, nullable=False)
    #mark = db.Column(db.Integer, db.CheckConstraint('mark <= 5')) 

