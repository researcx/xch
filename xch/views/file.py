import xch
from flask import send_from_directory
from werkzeug.utils import secure_filename

@xch.app.route('/<board>/<file>')
def serve_file(board, file):
    return send_from_directory(xch.app.root_path + "/uploads/", secure_filename(file))
