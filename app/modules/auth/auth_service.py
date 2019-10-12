from app.models import RevokedTokenModel
from app.modules.user import UserService
from flask_jwt_extended import create_access_token, create_refresh_token
from app.exceptions import UserNotExist, WrongCredentials

user_service = UserService()

class AuthService:
    def authenticate(self, username, password):
        user = user_service.find_by_username(username)
        if user is None:
            raise UserNotExist(username)
        if not user.check_password(password):
            raise WrongCredentials()

    def revoke_token(self, jti):
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.save_to_db()
    
    def create_access_token(self, identity):
        return create_access_token(identity=identity)

    def create_refresh_token(self, identity):
        return create_refresh_token(identity=identity)