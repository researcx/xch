import xch
from datetime import datetime, timedelta
import humanize
import time


intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )


SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
MONTH = 30 * DAY


#@xch.cache.memoize(timeout=60) # get_ban_expiry
def get_ban_expiry(unixtime):
    dt = datetime.fromtimestamp(unixtime)
    now = datetime.now()
    delta_time = dt - now

    delta =  delta_time.days * DAY + delta_time.seconds
    minutes = delta / MINUTE
    hours = delta / HOUR
    days = delta / DAY

    if delta <  0:
        return "EXPIRED"

    if delta < 1 * MINUTE:
      if delta == 1:
          return  "one second"
      else:
          return str(int(delta)) + " seconds"


    if delta < 2 * MINUTE:
        return str(int(minutes)) + " minutes"


    if delta < 45 * MINUTE:
        return str(int(minutes)) + " minutes"

    if delta < 90 * MINUTE:
        return str(int(minutes)) + " minutes"

    if delta < 24 * HOUR:
        return str(int(hours)) + " hours"

    if delta < 48 * HOUR:
        return str(int(hours)) + " hours"

    if delta < 30 * DAY:
        return str(int(days)) + " days"


    if delta < 12 * MONTH:
        months = delta / MONTH
        if months <= 1:
            return "one month"
        else:
            return str(int(months)) + " months"
    else:
      years = days / 365.0
      if  years <= 1:
          return "one year"
      else:
          return str(int(years)) + " years"
xch.app.jinja_env.globals.update(get_ban_expiry=get_ban_expiry)

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

#Code for the "page generation took x seconds" thing.
@xch.app.before_request
def before_request():
    xch.g.request_start_time = time.time()
    xch.g.request_time = lambda: "%.5f" % (time.time() - xch.g.request_start_time)

#Current time as a part of the code
@xch.app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

#Current time in UNIX format
def unix_time_current():
    return int(time.time())

#Display how long ago something happened in a readable format
@xch.app.template_filter('time_ago')
#@xch.cache.memoize(timeout=60) # time_ago
def time_ago(unixtime):
    return humanize.naturaltime(datetime.now() - timedelta(seconds=unix_time_current() - int(unixtime)))
xch.app.jinja_env.globals.update(time_ago=time_ago)

#Display a somewhat normal date
@xch.app.template_filter('human_date')
#@xch.cache.memoize(timeout=60) # human_date
def human_date(unixtime):
    return datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
xch.app.jinja_env.globals.update(human_date=human_date)

#Display a somewhat normal date for threads/channels
@xch.app.template_filter('recent_date')
#@xch.cache.memoize(timeout=60) # recent_date
def recent_date(unixtime):
    dt = datetime.fromtimestamp(unixtime)
    today = datetime.now()
    today_start = datetime(today.year, today.month, today.day)
    yesterday_start = datetime.now() - timedelta(days=1)

    def day_in_this_week(date):
        startday = datetime.now() - timedelta(days=today.weekday())
        if(date >= startday):
            return True
        else:
            return False

    timeformat = '%b %d, %Y'
    if day_in_this_week(dt):
        timeformat = '%A at %H:%M'
    if(dt >= yesterday_start):
        timeformat = 'Yesterday at %H:%M'
    if(dt >= today_start):
        timeformat = 'Today at %H:%M'

    return(dt.strftime(timeformat))
xch.app.jinja_env.globals.update(recent_date=recent_date)

#Display a somewhat normal size
@xch.app.template_filter('human_size')
#@xch.cache.memoize(timeout=60) # human_size
def human_size(filesize):
    return humanize.naturalsize(filesize)
xch.app.jinja_env.globals.update(human_size=human_size)


@xch.app.template_filter('get_filemtime')
#@xch.cache.memoize(timeout=60) # get_filemtime
def get_filemtime(file):
    filepath = xch.app.static_folder + file
    if xch.os.path.isfile(filepath):
        filetime = int(xch.os.stat(filepath).st_mtime)
        if filetime:
            return file + "?v=" + str(filetime)
    else:
        return file
xch.app.jinja_env.globals.update(get_filemtime=get_filemtime)