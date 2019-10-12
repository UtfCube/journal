from app import db
from .base import BaseModel

class Person(BaseModel):
    """Model for the persons"""
    __abstract__ = True

    fio = db.Column(db.String(200), nullable=False)