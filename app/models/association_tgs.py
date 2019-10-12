from app import db
from .base import BaseModel

class AssociationTGS(BaseModel):
    """Model for the tgs table"""
    __tablename__ = "tgs"

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.user_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    subject_name = db.Column(db.String(128), db.ForeignKey('subjects.name'), nullable=False)
    #checkpoints = db.relationship('Checkpoint', lazy='dynamic',
    #    backref=db.backref('tgs', lazy=True), cascade='all,delete-orphan') 
