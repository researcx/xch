import xch
from xch.models.sql.blotter import query_blotter

#@xch.cache.memoize(timeout=86400) # render_blotter_list
def render_blotter_list(count=3):
    render = ""
    blotter = query_blotter(count)
    if blotter:
        xch.logger.info("found blotter items" + str(blotter))
        for item in blotter:
            render += '''<tr>
                            <td data-utc="'''+str(item.time)+'''" class="blotter-date">'''+str(item.time)+'''</td>
                            <td class="blotter-content">'''+item.content+'''</td>
                        </tr>'''
    return render
xch.app.jinja_env.globals.update(render_blotter_list=render_blotter_list)
