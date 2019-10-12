from app import db
from .base import BaseModel

class Checkpoint(BaseModel):
    """Model for checkpoints table"""
    __tablename__ = "checkpoints"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    #tgs_id = db.Column(db.Integer, db.ForeignKey('tgs.id'), nullable=False)
    subject_name = db.Column(db.String(128), db.ForeignKey('subjects.name'), nullable=False)
    fields = db.relationship('CheckpointField', lazy='dynamic',
        backref=db.backref('checkpoint', lazy=True), passive_deletes=True) 