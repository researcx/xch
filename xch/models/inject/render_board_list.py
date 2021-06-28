import xch
from xch.models.sql.category import sql_category
from xch.models.sql.board import sql_board

#@xch.cache.memoize(timeout=86400) # render_board_list
def render_board_list():
    rendered_boards = []
    render = ""
    categories = sql_category.query.filter_by(public=1).all()
    if categories:
        render = ""
        xch.logger.info(str(categories))
        for category in categories:
            rendered_boards = []
            render += "["
            boards = sql_board.query.filter_by(cat=category.id).all()
            xch.logger.info(str(boards))
            for board in boards:
                rendered_boards.append('<a href="' + xch.config['site']['path'] + board.url + '/" title="' + board.title + '">' + board.url + '</a>')
            render += (' / '.join(rendered_boards))
            render += "]"
    return render
xch.app.jinja_env.globals.update(render_board_list=render_board_list)
