import xch, random

#@xch.cache.memoize(timeout=86400) # render_footer
def render_footer():
    footers = xch.config['site']['footers']
    random_index = random.randint(0,len(footers)-1)
    return footers[random_index]
xch.app.jinja_env.globals.update(render_footer=render_footer)

