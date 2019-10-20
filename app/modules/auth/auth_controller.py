from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt, jwt_refresh_token_required
from flask_restful import Resource
from app.parsers import user_login_parser
from app.decorators import expect
from .auth_service import AuthService

auth_service = AuthService()

class UserLogin(Resource):
    @expect(user_login_parser)
    def post(self, data):
        data = user_login_parser.parse_args()
        user = auth_service.authenticate(data['username'], data['password'])
        access_token = auth_service.create_access_token(identity=data['username'])
        refresh_token = auth_service.create_refresh_token(identity=data['username'])
        return {
            'role': user.role,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
            
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        auth_service.revoke_token(jti)
        return {'msg': 'Access token has been revoked'}

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        auth_service.revoke_token(jti)
        return {'msg': 'Refresh token has been revoked'}

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = auth_service.create_access_token(identity=current_user)
        return {'access_token': access_token}