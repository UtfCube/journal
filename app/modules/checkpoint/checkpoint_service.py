class CheckpointService:
    def from_csv(self, csv_list):
        for checkpoint_csv in csv_list:
            checkpoint = {}
            checkpoint_name = checkpoint_csv[0]
            checkpoint['name'] = checkpoint_name
            fields_csv = checkpoint_csv[1::]
            field_count = len(fields_csv)
            fields = []
            checkpoint['fields'] = fields
            fields.append({
                'name': 'Оценка',
                'type': '5'
            })
            fields.append({
                'name': 'Дата проведения'
            })
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
                if field_count > 1:
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

    def add(self, checkpoints):
        for checkpoint in checkpoints:
            pass