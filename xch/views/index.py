import xch

@xch.app.route("/")
def index():
    if xch.config['site']['single_board'] != "":
        return xch.redirect(xch.config['site']['single_board'])
    return xch.render_template('index_4ch.html', page_title="")

@xch.app.route("/boards")
def boards_list():
    if xch.config['site']['single_board'] != "":
        return xch.redirect(xch.config['site']['single_board'])
    return xch.render_template('index_8ch.html', page_title="")