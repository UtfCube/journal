from app import db
from .base import BaseModel

class Group(BaseModel):
    """Model for the groups table"""
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    students = db.relationship('Student', backref='group', lazy='dynamic')
    tgs = db.relationship('AssociationTGS', lazy='dynamic',
        backref=db.backref('group', lazy=True), cascade='all,delete-orphan')

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()