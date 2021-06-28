import xch
from xch.models.sql.board import query_board

@xch.app.route("/<board>/")
def board(board):
    xch.logger.info("accessing " + board)
    board_info = query_board(board)
    if board_info:
        xch.logger.info(str(board_info))
        return xch.render_template('board.html', page_title="/" + board_info.url + "/ - " + board_info.title, board=board_info)
    return "404"