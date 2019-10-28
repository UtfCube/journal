from app import db
from app.models import User
from app.exceptions import UserExist, UserNotExist, WrongCredentials
from app.utils import generate_password
from sqlalchemy import or_

class UserService:
    def find_by_username(self, username):
        return User.find_by_username(username)

    def create_user(self, username, password, role='student'):
        if self.find_by_username(username):
            raise UserExist(username)
        user = User(username, password, role)
        user.add_to_db()
        return user
    
    def change_password(self, username, password):
        user = self.find_by_username(username)
        user.change_password(password)
        db.session.commit()

    def generate_password(self, username):
        new_password = generate_password()
        self.change_password(username, new_password)
        return new_password

    def get_all_logins(self):
        users = User.query.filter(or_(User.role=='student', User.role=='tutor')).all()
        res = {
            "tutors": [],
            "students": []
        }
        for user in users:
            res['{}s'.format(user.role)].append({**user.json(['id', 'role', 'password_hash']), 'password': '***'})
        return res
        



