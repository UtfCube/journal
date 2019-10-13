from flask_restful import reqparse

CANNOT_BE_BLANK='This field cannot be blank'

tutor_reg_parser = reqparse.RequestParser()
tutor_reg_parser.add_argument('username', help=CANNOT_BE_BLANK, required=True)
tutor_reg_parser.add_argument('fio', help=CANNOT_BE_BLANK, required=True)
tutor_reg_parser.add_argument('role', help=CANNOT_BE_BLANK, required=True)

student_reg_parser = reqparse.RequestParser()
student_reg_parser.add_argument('username', help=CANNOT_BE_BLANK, required=True)
student_reg_parser.add_argument('fio', help=CANNOT_BE_BLANK, required=True)
student_reg_parser.add_argument('fullname', help=CANNOT_BE_BLANK, required=True)
student_reg_parser.add_argument('role', help=CANNOT_BE_BLANK, required=True)

user_login_parser = reqparse.RequestParser()
user_login_parser.add_argument('username', help=CANNOT_BE_BLANK, required=True)
user_login_parser.add_argument('password', help=CANNOT_BE_BLANK, required=True)

association_parser = reqparse.RequestParser()
association_parser.add_argument('subject_name', help=CANNOT_BE_BLANK, required=True)
association_parser.add_argument('group_id', type=int, required=True)
