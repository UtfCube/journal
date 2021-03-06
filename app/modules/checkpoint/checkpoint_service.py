from app import db
from app.exceptions import SubjectNotExist, CheckpointNotExist, CheckpointFieldNotExist
from app.models import Subject, Checkpoint, CheckpointField

dates_names = ['Дата проведения', 'Льготный срок сдачи', 'Крайний срок сдачи']

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
                    'name': 'Число попыток сдачи',
                    'type': "n"
                })
                fields.append({
                    'name': 'Дата сдачи',
                    'type': 'd'
                })
                fields.append({
                    'name': 'Льготный срок сдачи'
                })
                fields.append({
                    'name': 'Крайний срок сдачи'
                })

    def add_base_checkpoint(self, checkpoints):
        checkpoint = {
            "name": "",
            "fields": [
                {
                    "name": "Оценка за работу в семестре",
                    "type": "5"
                },
                {
                    "name": "Ведущий преподаватель",
                    "type": "p"
                },
                {
                    "name": "Признаки плагиата",
                    "is_hidden": True
                }
                
            ]
        }
        checkpoints.append(checkpoint)

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
        self.add_base_fields(checkpoints_json)
        self.add_base_checkpoint(checkpoints_json)
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

    def delete(self, subject_name, checkpoints_names):
        subject = Subject.query.filter_by(name=subject_name).first()
        if subject is None: 
            raise SubjectNotExist(subject_name)
        for checkpoint_name in checkpoints_names:
            subject.checkpoints.filter_by(name=checkpoint_name).delete()
        db.session.commit()

    def get_all(self, subject_name):
        subject = Subject.query.filter_by(name=subject_name).first()
        if subject is None: 
            raise SubjectNotExist(subject_name)
        checkpoints = subject.checkpoints.all()
        res = Checkpoint.json_list(checkpoints, ['id', 'subject_name'])
        for i, checkpoint in enumerate(checkpoints):
            fields = checkpoint.fields.all()
            res[i]['fields'] = [ field.json(['id', 'checkpoint_id']) for field in fields if field.name not in dates_names]
            res[i]['dates'] = [ field.json(['id', 'checkpoint_id']) for field in fields if field.name in dates_names]
            for field in fields:
                date_info = field.dates_info.first()
                if date_info is not None:
                    for json_date in res[i]['dates']:
                        if json_date['name'] == field.name:
                            json_date['date'] = date_info.date
        return res
    
    def find_field_by_name(self, subject_name, checkpoint_name, field_name):
        subject = Subject.query.filter_by(name=subject_name).first()
        if subject is None: 
            raise SubjectNotExist(subject_name)
        checkpoint = subject.checkpoints.filter_by(name=checkpoint_name).first()
        if checkpoint is None:
            raise CheckpointNotExist(checkpoint_name)
        field = checkpoint.fields.filter_by(name=field_name).first()
        if field is None:
            raise CheckpointFieldNotExist(checkpoint_name, field_name)
        return field