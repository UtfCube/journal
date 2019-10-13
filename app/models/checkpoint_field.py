from app import db
from .base import BaseModel

class CheckpointField(BaseModel):
    """Model for checkpoints_fields table"""
    __tablename__ = "checkpoints_fields"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoints.id', ondelete='CASCADE'), nullable=False)
    is_hidden = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(1), nullable=True)
    dates_info = db.relationship('DatesInfo', lazy='dynamic',
        backref=db.backref('checkpoint_field', lazy=True), passive_deletes=True)
    progress = db.relationship('Progress', lazy='dynamic',
        backref=db.backref('checkpoint_field', lazy=True), passive_deletes=True)