import secrets
import string
from werkzeug.utils import secure_filename
import os

def generate_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(8))


def save_file(folder, file):
    filename = secure_filename(file.filename)
    path = os.path.join(folder, filename)
    file.save(path)
    return path