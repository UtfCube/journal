from .student_service import StudentService
from .tutor_service import TutorService
from .user_service import UserService
from .token_service import TokenService
from .admin_service import AdminService

user_service = UserService()
student_service = StudentService()
tutor_service = TutorService()
token_service = TokenService()
admin_service = AdminService()