import xch
from slugify import slugify

#@xch.cache.memoize(timeout=86400) # get_slug
def get_slug(title):
    if title:
        return slugify(title, max_length=50, separator='_', lowercase=True)
    return "_"
xch.app.jinja_env.globals.update(get_slug=get_slug)
