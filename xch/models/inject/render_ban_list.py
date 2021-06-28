import xch
from xch.models.sql.bans import sql_bans
from xch.models.sql.staff import sql_mods
from xch.models.inject.time import display_time, get_ban_expiry, recent_date
from xch.models.inject.parse_ip import parse_ip


#@xch.cache.memoize(timeout=86400) # render_ban_list
def render_ban_list(board="wg"):
    bans = sql_bans.query.filter(sql_bans.display != 0).all()
    ban_list = ""
    rendered_boards = []
    ban_boards = "ALL"

    for ban in bans:
        if ban.board != "*":
            board_list = ban.board.split(",")
            for board in board_list:
                rendered_boards.append('<a href="' + xch.config['site']['path'] + board + '/" title="' + board + '">' + board + '</a>')
    if len(rendered_boards) >= 1: 
        ban_boards = (' / '.join(rendered_boards))

    for ban in bans:
        if ban.length is not 0:
            ban_duration = display_time(ban.length)
            time_left = get_ban_expiry(ban.expires)
        else:
            ban_duration = "FOREVER"
            time_left = "NEVER"
        if ban.length is -1:
            ban_duration = "UNBANNED"
            time_left = "EXPIRED"

        ban_list += '''<tr>
                        <td>'''+recent_date(ban.time)+'''</td>
                        <td>'''+parse_ip(ban.user)+'''</td>
                        <td>['''+ban_boards+''']</td>
                        <td>'''+ban.reason+'''</td>
                        <td>'''+ban_duration+'''</td>
                        <td>'''+time_left+'''</td>
                        <td>'''+ban.moderator+'''</a></td>
                    </tr>'''

    return ban_list
xch.app.jinja_env.globals.update(render_ban_list=render_ban_list)