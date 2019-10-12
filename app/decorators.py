from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.modules.user import UserService
from app.exceptions import UserIsNotAdmin
from typing import Union

user_service = UserService()

def auth_user(func):
    @wraps(func)
    @jwt_required
    def wrapper(self, *args, **kwargs):
        current_user = get_jwt_identity()
        return func(self, current_user, *args, **kwargs)
    return wrapper

def is_role(roles: Union[str, list]):
    def decorator(func):
        @wraps(func)
        def wrapper(self, current_user, *args, **kwargs):
            user = user_service.find_by_username(current_user)
            if isinstance(roles, str):   
                if user.role == roles:
                    return func(self, current_user, *args, **kwargs)
                else:
                    raise UserIsNotAdmin(current_user)
            else:
                for role in roles:
                    if user.role == role:
                        return func(self, current_user, *args, **kwargs)
                raise UserIsNotAdmin(current_user)
        return wrapper
    return decorator

def expect(validator):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            data = validator.parse_args()
            return func(self, *args, data, **kwargs)
        return wrapper
    return decorator