import xch, re, ast

def query_post(post=None):
    options = sql_post.query.filter_by(id=post).first()
    if options:
        xch.logger.info(str(options))
        return options
    return []

def query_thread(post=None):
    options = sql_post.query.filter_by(id=post).filter_by(thread=0).first()
    if options:
        xch.logger.info(str(options))
        return options
    return []


def replies_to_post(post_id=None, thread_id=None):
    xch.logger.info("trying to find replies for post " + str(post_id) + " filtered by thread id " + str(thread_id))
    all_posts = sql_post.query.filter_by(thread=thread_id).all()
    repliers = []
    for post in all_posts:
        reply_list = ast.literal_eval(post.reply_to)
        xch.logger.info("searching_for" + str(post_id))
        xch.logger.info("reply_list " + str(reply_list))
        if str(post_id) in reply_list:
            xch.logger.info("post that's replying to the:")
            xch.logger.info(str(post.id))
            repliers.append(post.id)
    return repliers


def replies_in_content(content):
    m = re.findall('>>(\d+)', content, re.IGNORECASE|re.MULTILINE)
    if m:
        xch.logger.info(m)
        return m
    return False


class sql_post(xch.db.Model):
    id = xch.db.Column(xch.db.Integer, primary_key=True)
    time = xch.db.Column(xch.db.Integer, unique=False, default=0)
    content = xch.db.Column(xch.db.String, unique=False)
    title = xch.db.Column(xch.db.String, unique=False)
    poster = xch.db.Column(xch.db.String, unique=False)
    poster_id = xch.db.Column(xch.db.String, unique=False)
    poster_ip = xch.db.Column(xch.db.String, unique=False)
    poster_location = xch.db.Column(xch.db.String, unique=False)
    file = xch.db.Column(xch.db.String, unique=False)
    options = xch.db.Column(xch.db.String, unique=False)
    board = xch.db.Column(xch.db.Integer, unique=False, default=0)
    thread = xch.db.Column(xch.db.Integer, unique=False, default=0)
    reply_to = xch.db.Column(xch.db.String, unique=False, default=0)
    is_sticky = xch.db.Column(xch.db.Integer, unique=False, default=0)
    is_closed = xch.db.Column(xch.db.Integer, unique=False, default=0)
    is_archived = xch.db.Column(xch.db.Integer, unique=False, default=0)
    
    def __repr__(self):
        return '<Post %r>' % self.id