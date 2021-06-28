import xch
from datetime import datetime, timedelta

#@xch.cache.memoize(timeout=86400) # render_human_time
def render_human_time(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d(%a)%H:%M:%S')
xch.app.jinja_env.globals.update(render_human_time=render_human_time)

