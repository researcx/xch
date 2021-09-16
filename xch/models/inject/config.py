import xch

#Get core config variables
#@xch.cache.memoize(timeout=86400) # config
def config():
    if xch.request.headers.get('Host'):
        xch.config['site']['url'] = "https://" + xch.request.headers.get('Host')
    return xch.config
xch.app.jinja_env.globals.update(config=config)

#@xch.cache.memoize(timeout=86400) # get_site_url
def get_site_url():
    if xch.request.headers.get('Host'):
        site_url = "https://" + xch.request.headers.get('Host') + "/"
    else:
        site_url = xch.config['site']['url']
    return site_url
xch.app.jinja_env.globals.update(get_site_url=get_site_url)
