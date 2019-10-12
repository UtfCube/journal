from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt, jwt_refresh_token_required
from flask_restful import Resource
from app.parsers import user_login_parser
from app.decorators import expect
from app.exceptions import BaseException, InternalError
from .auth_service import AuthService

auth_service = AuthService()

class UserLogin(Resource):
    @expect(user_login_parser)
    def post(self, data):
        data = user_login_parser.parse_args()
        try:
            auth_service.authenticate(data['username'], data['password'])
            access_token = auth_service.create_access_token(identity=data['username'])
            refresh_token = auth_service.create_refresh_token(identity=data['username'])
            return {
                'msg': 'Logged in as {}'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()
            
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            auth_service.revoke_token(jti)
            return {'msg': 'Access token has been revoked'}
        except Exception as e:
            print(e)
            return InternalError().to_json()

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            auth_service.revoke_token(jti)
            return {'msg': 'Refresh token has been revoked'}
        except Exception as e:
            print(e)
            return InternalError().to_json()

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = auth_service.create_access_token(identity=current_user)
        return {'access_token': access_token}