from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User, Subject, Group

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегестрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Этот логин уже зарегестрирован. Попробуйте другой.')

class PersonInfoForm(FlaskForm):
    lastname = StringField('Фамилия')
    firstname = StringField('Имя')
    patronymic = StringField('Отчество')
    rank = StringField('Звание')

class TutorInfoForm(PersonInfoForm):
    degree = StringField('Ученая степень')

class StudentInfoForm(PersonInfoForm):
    admission_year = IntegerField('Дата поступления')
    group_id = IntegerField('Номер группы')

class TutorRegistrationForm(TutorInfoForm, RegistrationForm):
    def __init__(self):
        TutorInfoForm.__init__(self)
        RegistrationForm.__init__(self)
        for field in (self.lastname, self.firstname, self.patronymic, self.rank, self.degree):
            field.validators = [DataRequired()]

class StudentRegistrationForm(StudentInfoForm, RegistrationForm):
    def __init__(self):
        StudentInfoForm.__init__(self)
        RegistrationForm.__init__(self)
        for field in (self.lastname, self.firstname, self.patronymic, self.rank, self.admission_year, self.group_id):
            field.validators = [DataRequired()]

class SubjectsEditForm(FlaskForm):
    subject = StringField('Предмет', validators=[DataRequired()])
    group_id = IntegerField('Группа', validators=[DataRequired()])
    add = SubmitField('Добавить')
    delete = SubmitField('Удалить')


    def validate_add(self, add):
        if add.data:
            if current_user.tutor.tgs.filter_by(group_id=self.group_id.data, subject_name=self.subject.data).first() is not None:
                raise ValidationError("Эта пара уже добавлена. Попробуйте снова.")

    def validate_delete(self, delete):
        if delete.data:
            if current_user.tutor.tgs.filter_by(group_id=self.group_id.data, subject_name=self.subject.data).first() is None:
                raise ValidationError("Этой пары не существует. Попробуйте снова.")

class CheckPointForm(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
    posting_date = DateField('Дата сдачи', validators=[DataRequired()])
    critical_date = DateField('Крайняя дата сдачи', validators=[DataRequired()])
    submit = SubmitField('Изменить') 


