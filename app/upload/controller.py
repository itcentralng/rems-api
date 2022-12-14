from flask import Blueprint, request
from app.route_guard import auth_required

from app.upload.model import *
from app.upload.schema import *
from helpers.upload_helper import do_upload
bp = Blueprint('upload', __name__)

@bp.post('/upload')
@auth_required("admin")
def upload_new_file():
    file = request.files.get('file')
    if file is None:
        return {'message': 'File is required'}, 400
    else:
        url = do_upload(file)
        return {'url': url}, 200