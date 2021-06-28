import xch
from flask import send_from_directory

@xch.app.route('/index/<page>')
def serve_page(page):
    return xch.render_template("pages/" + page + ".html", page_title=page)
