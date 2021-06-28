import xch, re
from xch.models.sql.post import replies_in_content
from markdown2 import Markdown
import xch.models.inject.bbcode


#@xch.cache.memoize(timeout=86400) # parse_message
def parse_message(message=None, length=0, formatting=1):
    markdowner = Markdown()
    #if Settings.USE_MARKDOWN:
    #if not Settings.USE_MARKDOWN:
    message = message.replace("\r", "<br />")
    #message = markdowner.convert(message)
    #message = xch.models.inject.bbcode.parser.format(message)

    message = re.sub('(>>(\d+))', r'<br /><a href="#p\g<2>" class="quotelink">&gt;&gt;\g<2></a><br />', message)
    message = re.sub('(>([^\n]*$))', r'<br /><span class="quote">&gt;\g<2></span><br />', message)
    return message
    #return message
xch.app.jinja_env.globals.update(parse_message=parse_message)
