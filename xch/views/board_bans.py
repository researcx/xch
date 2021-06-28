import xch
from xch.models.sql.board import query_board
from xch.models.inject.render_ban_list import render_ban_list

@xch.app.route("/<board>/bans")
def board_bans(board):
    xch.logger.info("accessing bans list for " + board)
    if board == "*":
        ban_list = render_ban_list("*")
        return xch.render_template('ban_list.html', page_title="All Boards - Ban List", ban_list=ban_list,board=[])
    board_info = query_board(board)
    if board_info:
        ban_list = render_ban_list(board_info.url)
        xch.logger.info(str(board_info))
        return xch.render_template('ban_list.html', page_title="/" + board_info.url + "/ - " + board_info.title, ban_list=ban_list,board=board_info)
    return "404"