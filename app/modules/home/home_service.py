from app.modules.user import UserService
from app.modules.admin import AdminService
from app.modules.tutor import TutorService
from app.modules.student import StudentService

user_service = UserService()
admin_service = AdminService()
tutor_service = TutorService()
student_service = StudentService()

class HomeService:
    def get(self, current_user):
        user = user_service.find_by_username(current_user)
        if user.role == 'tutor':
            return tutor_service.get_home_info(current_user)
        elif user.role == 'student':
            return student_service.get_home_info(current_user)
        else:
            return admin_service.get_home_info()