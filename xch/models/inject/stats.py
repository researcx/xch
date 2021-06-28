import xch, psutil
from xch.models.sql.bans import sql_bans
from xch.models.sql.post import sql_post
from xch.models.sql.board import sql_board

#@xch.cache.memoize(timeout=360) # stats
def stats():
    #User Count (by unique id)
    user_count = sql_post.query.filter(sql_post.thread != 0).count()
    #Post Count
    post_count = sql_post.query.filter(sql_post.thread != 0).count()
    #Thread Count
    thread_count = sql_post.query.filter(sql_post.thread == 0).count()
    #Ban Count
    ban_count = sql_bans.query.count()

    #Forum/Channel Count
    official_board_count = sql_board.query.filter(sql_board.owned_by == "").count()
    unofficial_board_count = sql_board.query.filter(sql_board.owned_by != "").count()
    unapproved_board_count = sql_board.query.filter(sql_board.approved_by == "").count()

    #Server Statistics
    cpu_percentage = psutil.cpu_percent()

    disk_total, disk_used, disk_free, disk_percentage = psutil.disk_usage('/')

    mem = psutil.virtual_memory()
    memory_total = mem.total
    memory_used = mem.used
    memory_percentage = mem.percent

    #Progress Indicators
    if int(cpu_percentage) <= 50:
        cpu_indicator = "progress-bar-success"
    if int(cpu_percentage) >= 50:
        cpu_indicator = "progress-bar-info"
    if int(cpu_percentage) >= 70:
        cpu_indicator = "progress-bar-warning"
    if int(cpu_percentage) >= 90:
        cpu_indicator = "progress-bar-danger"

    if int(disk_percentage) <= 50:
        disk_indicator = "progress-bar-success"
    if int(disk_percentage) >= 50:
        disk_indicator = "progress-bar-info"
    if int(disk_percentage) >= 70:
        disk_indicator = "progress-bar-warning"
    if int(disk_percentage) >= 90:
        disk_indicator = "progress-bar-danger"

    if int(memory_percentage) <= 50:
        memory_indicator = "progress-bar-success"
    if int(memory_percentage) >= 50:
        memory_indicator = "progress-bar-info"
    if int(memory_percentage) >= 70:
        memory_indicator = "progress-bar-warning"
    if int(memory_percentage) >= 90:
        memory_indicator = "progress-bar-danger"

    return {'user_count': user_count, 'post_count': post_count, 'thread_count': thread_count, 'ban_count': ban_count, 'official_board_count': official_board_count, 'unofficial_board_count': unofficial_board_count, 'unapproved_board_count': unapproved_board_count, 'disk_total': disk_total, 'disk_used': disk_used, 'disk_percentage': disk_percentage, 'memory_total': memory_total, 'memory_used': memory_used, 'cpu_percentage': cpu_percentage, 'cpu_indicator': cpu_indicator, 'disk_indicator': disk_indicator, 'memory_indicator': memory_indicator}
xch.app.jinja_env.globals.update(stats=stats)