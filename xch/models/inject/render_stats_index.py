import xch
from xch.models.sql.category import sql_category
from xch.models.sql.board import sql_board

								# <div class="stat-cell"><b>Total Posts:</b> 3,718,563,524</div>
								# <div class="stat-cell"><b>Current Users:</b> 221,197</div>
								# <div class="stat-cell"><b>Active Content:</b> 1363 GB</div>

#@xch.cache.memoize(timeout=86400) # render_stats_index
def render_stats_index():
    rendered_threads = []
    render = '''<div class="stat-cell"><b>Total Posts:</b> 3,718,563,524</div>
                <div class="stat-cell"><b>Current Users:</b> 221,197</div>
                <div class="stat-cell"><b>Active Content:</b> 1363 GB</div>'''
    return render

xch.app.jinja_env.globals.update(render_stats_index=render_stats_index)
