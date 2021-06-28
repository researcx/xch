import xch, random

#@xch.cache.memoize(timeout=86400) # render_banner
def render_banner():
    banners = xch.config['site']['banners']
    random_index = random.randint(0,len(banners)-1)
    return banners[random_index]
xch.app.jinja_env.globals.update(render_banner=render_banner)

