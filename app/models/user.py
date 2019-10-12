from app import db
from .base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    """Model for the users table"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default='student')
    tutor = db.relationship('Tutor', backref='account', uselist=False, lazy=True)
    student = db.relationship('Student', backref='account', uselist=False, lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)