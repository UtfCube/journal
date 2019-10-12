from app import db
from app.exceptions import SubjectNotExist
from app.models import Subject, Checkpoint, CheckpointField

class CheckpointService:
    def add_base_fields(self, checkpoints):
        for checkpoint in checkpoints:
            fields = checkpoint['fields']
            field_num = len(fields)
            fields.append({
                'name': 'Оценка',
                'type': '5'
            })
            fields.append({
                'name': 'Дата проведения'
            })
            if field_num > 1:
                fields.append({
                    'name': 'Число попыток сдачи'
                })
                fields.append({
                    'name': 'Дата сдачи'
                })
                fields.append({
                    'name': 'Льготный срок сдачи'
                })
                fields.append({
                    'name': 'Крайний срок сдачи'
                })
            yield checkpoint

    def from_csv(self, csv_list):
        for checkpoint_csv in csv_list:
            checkpoint = {}
            checkpoint_name = checkpoint_csv[0]
            checkpoint['name'] = checkpoint_name
            fields_csv = checkpoint_csv[1::]
            field_count = len(fields_csv)
            fields = []
            checkpoint['fields'] = fields
            if field_count > 0:
                for field_name in fields_csv:
                    field = {}
                    clean_field_name = field_name.replace('*', '').replace('+', '').replace('5', '')    
                    field['name'] = clean_field_name
                    if field_name.startswith('*'):
                        field['is_hidden'] = True
                    if field_name.endswith('+'):
                        field['type'] = '+'
                    elif field_name.endswith('5'):
                        field['type'] = '5'
                    fields.append(field)
            yield checkpoint

    def add(self, subject_name, checkpoints_json):
        checkpoints_json = self.add_base_fields(checkpoints_json)
        subject = Subject.query.filter_by(name=subject_name).first()
        if subject is None: 
            subject = Subject(name=subject_name)
            subject.add_to_db()
        checkpoints = subject.checkpoints
        for checkpoint_json in checkpoints_json:
            checkpoint_name =  checkpoint_json['name']
            checkpoint = checkpoints.filter_by(name=checkpoint_name).first()
            if checkpoint is None:
                checkpoint = Checkpoint(name=checkpoint_name)
                checkpoints.append(checkpoint)
            fields = checkpoint.fields
            for field_json in checkpoint_json['fields']:
                field_name = field_json['name']
                field = fields.filter_by(name=field_name).first()
                if field is None:
                    field = CheckpointField(name=field_name)
                    fields.append(field)
                field.type = field_json.get('type', None)
                field.is_hidden = field_json.get('is_hidden', False)
        db.session.commit()
        checkpoints = subject.checkpoints.all()
        return Checkpoint.json_list(checkpoints)

    def delete(self, subject_name, checkpoints_ids):
        subject = Subject.query.filter_by(name=subject_name).first()
        if subject is None: 
            raise SubjectNotExist(subject_name)
        for checkpoints_id in checkpoints_ids:
            subject.checkpoints.filter_by(id=checkpoints_id).delete()
        db.session.commit()