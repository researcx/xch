import xch

#@xch.cache.memoize(timeout=86400) # compose_title
def compose_title(title):
    if title:
        return title + " - " + xch.config['site']['title']
    else:
        return xch.config['site']['title']
xch.app.jinja_env.globals.update(compose_title=compose_title)
