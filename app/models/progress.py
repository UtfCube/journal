from app import db
from .base import BaseModel

class Progress(BaseModel):
    """Model for the progress table"""
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.user_id'), nullable=False)
    checkpoint_field_id = db.Column(db.Integer, db.ForeignKey('checkpoints_fields.id', ondelete='CASCADE'), nullable=False)
    result = db.Column(db.String(40))