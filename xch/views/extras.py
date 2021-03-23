import xch
from flask import send_from_directory

@xch.app.route('/robots.txt')
def robotstxt():
    return send_from_directory(xch.app.static_folder, xch.request.path[1:])

@xch.app.route('/favicon.ico')
def faviconico():
    return send_from_directory(xch.app.static_folder, xch.request.path[1:])
