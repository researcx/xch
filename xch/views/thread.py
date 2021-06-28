import xch
from xch.models.sql.board import query_board
from xch.models.sql.post import query_thread

@xch.app.route("/<board>/thread/<id>")
@xch.app.route("/<board>/thread/<id>/<slug>")
def thread(board, id, slug=""):
    xch.logger.info("accessing " + board)
    board_info = query_board(board)
    if board_info:
        xch.logger.info(str(board_info))
        xch.logger.info("accessing thread " + id)
        thread_info = query_thread(id)
        if thread_info:
            xch.logger.info(str(thread_info))
            return xch.render_template('thread.html', page_title="/" + board_info.url + "/ - " + thread_info.title + " - " + board_info.title, board=board_info, thread=thread_info)
    return "404"