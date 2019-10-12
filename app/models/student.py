from app import db
from .person import Person
from .progress import Progress
from sqlalchemy.event import listens_for

class Student(Person):
    """Model for the students table"""
    __tablename__ = "students"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=False, nullable=False)
    fullname = db.Column(db.String(30), nullable=False)
    admission_year = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    progress = db.relationship('Progress', backref=db.backref('student', lazy=True), lazy='dynamic', cascade='all,delete-orphan')

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()

@listens_for(Student, 'after_insert')
def add_group_checkpoints(mapper, connect, self):
    """trigger for the student model, that adds progress on existing checkpoints to a newly registered student"""
    student_id = (db.session.query(Student.user_id)
                    .filter(Student.group_id==self.group_id)).first()[0]
    cp_fields_ids = (db.session.query(Progress.checkpoint_field_id)
                .filter(Progress.student_id==student_id)).all()
    for id in cp_fields_ids:
        progress = Progress(checkpoint_field_id=id,
                            student_id=self.user_id)
        self.progress.append(progress)