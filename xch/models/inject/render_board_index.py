import xch
from xch.models.sql.category import sql_category
from xch.models.sql.board import sql_board


#@xch.cache.memoize(timeout=86400) # render_board_index
def render_board_index():
    rendered_boards = []
    render = "[]"
    categories = sql_category.query.all()
    if categories:
        render = ""
        xch.logger.info(str(categories))
        for category in categories:
            rendered_boards = []
            render += '<h3 style="text-decoration: underline; display: inline;">'+category.title+'</h3>'
            if category.nsfw:
                render += '''<h3 style="display: inline;">
                                <span class="warning" title="Not Safe For Work">
                                    <sup style="vertical-align: text-bottom;">(NSFW)</sup>
                                </span>
                            </h3>'''
            boards = sql_board.query.filter_by(cat=category.id).all()
            xch.logger.info(str(boards))
            for board in boards:
                render += '<li><a href="' + xch.config['site']['path'] + board.url + '/" class="boardlink">'+board.title+'</a></li>'
    return render
xch.app.jinja_env.globals.update(render_board_index=render_board_index)
