from app.models import User
from app.exceptions import UserExist, UserNotExist, WrongCredentials

class UserService:
    def find_by_username(self, username):
        return User.find_by_username(username)

    def create_user(self, username, password):
        if self.find_by_username(username):
            raise UserExist(username)
        user = User(username, password)
        user.add_to_db()
        return user

