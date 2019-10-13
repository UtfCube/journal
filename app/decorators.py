from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.modules.user import UserService
from app.exceptions import UserIsNotRole, DataNotValid
from typing import Union, List
from flask_restful.reqparse import RequestParser


user_service = UserService()

def auth_user(func):
    @wraps(func)
    @jwt_required
    def wrapper(self, *args, **kwargs):
        current_user = get_jwt_identity()
        return func(self, current_user, *args, **kwargs)
    return wrapper

def is_role(roles: Union[str, List[str]]):
    def decorator(func):
        @wraps(func)
        def wrapper(self, current_user, *args, **kwargs):
            user = user_service.find_by_username(current_user)
            if isinstance(roles, str):   
                if user.role == roles:
                    return func(self, current_user, *args, **kwargs)
                else:
                    return UserIsNotRole(current_user).to_json()
            else:
                for role in roles:
                    if user.role == role:
                        return func(self, current_user, *args, **kwargs)
                return UserIsNotRole(current_user).to_json()
        return wrapper
    return decorator

def expect(validator: Union[RequestParser, List[RequestParser]]):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if isinstance(validator, RequestParser):
                data = validator.parse_args()
                return func(self, *args, data, **kwargs)
            else:
                for v in validator:
                    try:
                        data = validator.parse_args()
                        return func(self, *args, data, **kwargs)
                    except:
                        continue
                    return DataNotValid().to_json()
        return wrapper
    return decorator