from app import db
from .base import BaseModel

class GroupInfo(BaseModel):
    """Model for groups_info table"""
    __tablename__ = "groups_info"

    id = db.Column(db.Integer, primary_key=True)
    tgs_id = db.Column(db.Integer, db.ForeignKey('tgs.id'), nullable=False)
    dates = db.relationship('DatesInfo', lazy='dynamic',
        backref=db.backref('group_info', lazy=True), passive_deletes=True)
    #name = db.Column(db.String(40), nullable=False)
    #subject_name = db.Column(db.String(128), db.ForeignKey('subjects.name'), nullable=False)
    #fields = db.relationship('CheckpointField', lazy='dynamic',
    #    backref=db.backref('checkpoint', lazy=True), passive_deletes=True) 