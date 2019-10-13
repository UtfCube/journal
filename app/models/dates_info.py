from app import db
from .base import BaseModel

class DatesInfo(BaseModel):
    """Model for dates_info table"""
    __tablename__ = "dates_info"

    id = db.Column(db.Integer, primary_key=True)
    group_info_id = db.Column(db.Integer, db.ForeignKey('groups_info.id', ondelete='CASCADE'), nullable=False)
    date_field_id = db.Column(db.Integer, db.ForeignKey('checkpoints_fields.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.String(40))