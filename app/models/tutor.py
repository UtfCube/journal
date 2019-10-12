from app import db
from .person import Person

class Tutor(Person):
    """Model for the tutors table"""
    __tablename__ = "tutors"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=False, nullable=False)
    tgs = db.relationship('AssociationTGS', lazy='dynamic',
        backref=db.backref('tutor', lazy=True), cascade='all,delete-orphan')
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()