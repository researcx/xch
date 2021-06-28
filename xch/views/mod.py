import xch
from xch.models.sql.staff import query_staff, sql_mods


@xch.app.route("/mod")
def mod_panel():
    xch.logger.info("accessing mod panel")
    post_info = query_staff('U6UiFMlcWsZ2LmMQRjAm') # admins securetripcode #lol#dicks
    xch.logger.info("mod: "+ str(post_info))
    if post_info:
        xch.logger.info(str(post_info))
        #print(vars(sql_mods))
        for item in vars(post_info):
            print(item)
        for item in vars(sql_mods):
            if item[0] != '_':
                print(item)
        return "logged in as " + str(post_info.name)
    return "404"