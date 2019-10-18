from app import db
from .base import BaseModel

class GroupInfo(BaseModel):
    """Model for groups_info table"""
    __tablename__ = "groups_info"

    id = db.Column(db.Integer, primary_key=True)
    tgs_id = db.Column(db.Integer, db.ForeignKey('tgs.id'), nullable=False)
    dates = db.relationship('DatesInfo', lazy='dynamic',
        backref=db.backref('group_info', lazy=True), passive_deletes=True)