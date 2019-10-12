from app import db
from .base import BaseModel

class Subject(BaseModel):
    """Model for the subjects table"""
    __tablename__ = "subjects"

    name = db.Column(db.String(128), primary_key=True)
    tgs = db.relationship('AssociationTGS', lazy='dynamic',
        backref=db.backref('subject', lazy=True), cascade='all,delete-orphan') 
    checkpoints = db.relationship('Checkpoint', lazy='dynamic',
        backref=db.backref('subject', lazy=True), cascade='all,delete-orphan') 
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()