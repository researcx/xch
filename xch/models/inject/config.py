import xch

#Get core config variables
#@xch.cache.memoize(timeout=86400) # config
def config():
    return xch.config
xch.app.jinja_env.globals.update(config=config)
