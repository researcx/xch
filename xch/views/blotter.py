import xch
from xch.models.sql.blotter import query_blotter

@xch.app.route("/blotter/")
def blotter():
    render = ""
    blotter = query_blotter()
    if blotter:
        xch.logger.info("found blotter items" + str(blotter))
        for item in blotter:
            render += '''<tr>
                            <td data-utc="'''+str(item.time)+'''" class="blotter-date">'''+str(item.time)+'''</td>
                            <td class="blotter-content">'''+item.content+'''</td>
                        </tr>'''
    return render