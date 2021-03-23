import xch

# viewable pages
@xch.app.route("/")
def index():
    return xch.render_template('index.html')
