import xch
from xch.models.sql.post import query_post

@xch.app.route("/post/<post>")
def post(post):
    xch.logger.info("accessing post " + post)
    post_info = query_post(post)
    xch.logger.info("Post: "+ str(post_info))
    if post_info:
        xch.logger.info(str(post_info))
        return str(post_info.id) + ": " + post_info.content
    return "404"