from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate  import Migrate
from flask_cors import CORS
from app.exceptions import BaseException, InternalError

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config.from_object(Config)
app.config['PROPAGATE_EXCEPTIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

@app.errorhandler(Exception)
def error_handler(e):
    if isinstance(e, BaseException):
        return e.to_json()
    else:
        print(e)
        return InternalError().to_json()

from app import views, utils, modules, models, parsers, exceptions

api.add_resource(modules.UserRegistration, '/api/register')
api.add_resource(modules.UserLogin, '/api/login')
api.add_resource(modules.UserLogoutAccess, '/api/logout/access')
api.add_resource(modules.UserLogoutRefresh, '/api/logout/refresh')
api.add_resource(modules.TokenRefresh, '/api/token/refresh')
api.add_resource(modules.TutorHome, '/api/tutor/home')
api.add_resource(modules.GroupSubject, '/api/associations')
api.add_resource(modules.ChangePassword, '/api/password')
#api.add_resource(resources.GroupCpProgress, '/api/tutor/<subject>/<group_id>/<cp_name>')
api.add_resource(modules.Checkpoints, '/api/<subject>/checkpoints')
api.add_resource(modules.Dates, '/api/<subject>/<group_id>/<cp_name>/dates')
api.add_resource(modules.StudentHome, '/api/student/home')
#api.add_resource(resources.SubjectProgress, '/api/student/<subject>')
api.add_resource(modules.AdminHome, '/api/admin/home')