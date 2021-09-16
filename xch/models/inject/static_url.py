import xch

#@xch.cache.memoize(timeout=86400) # static_url
def static_url(file_path):
    if xch.request.headers.get('Host'):
        static_url = "https://" + xch.request.headers.get('Host')
    else:
        static_url = xch.config['site']['static_url']
    mtime = ""
    file = xch.app.static_folder +  "/" + file_path
    xch.logger.info(f"* trying to access file path {file}.")
    if xch.os.path.isfile(file):
        file_time = int(xch.os.stat(file).st_mtime)
        if file_time:
            mtime =  "?v=" + str(file_time)
    url = static_url + xch.config['site']['static_folder'] + file_path + mtime
    return url
xch.app.jinja_env.globals.update(static_url=static_url)
