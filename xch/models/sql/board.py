import xch

def query_board(board=None):
    options = sql_board.query.filter_by(url=board).first()
    if options:
        xch.logger.info(str(options))
        return options
    return []

class sql_board(xch.db.Model):
    id = xch.db.Column(xch.db.Integer, primary_key=True)
    cat = xch.db.Column(xch.db.Integer, primary_key=False)
    title = xch.db.Column(xch.db.String, unique=True)
    url = xch.db.Column(xch.db.String, unique=True)
    description = xch.db.Column(xch.db.String, unique=False)
    password = xch.db.Column(xch.db.String, unique=False)
    r9k_mode = xch.db.Column(xch.db.Integer, unique=False, default=0)
    captcha = xch.db.Column(xch.db.Integer, unique=False, default=0)
    nsfw = xch.db.Column(xch.db.Integer, unique=False, default=0)
    show_location = xch.db.Column(xch.db.Integer, unique=False, default=0)
    random_names = xch.db.Column(xch.db.Integer, unique=False, default=0)
    thread_cooldown = xch.db.Column(xch.db.Integer, unique=False, default=60)
    reply_cooldown = xch.db.Column(xch.db.Integer, unique=False, default=10)
    upload_cooldown = xch.db.Column(xch.db.Integer, unique=False, default=10)
    approved_by = xch.db.Column(xch.db.String, unique=False, default="")
    owned_by = xch.db.Column(xch.db.String, unique=False, default="")
    public_bans = xch.db.Column(xch.db.Integer, unique=False, default=0)
    maxFilesize = xch.db.Column(xch.db.Integer, unique=False, default=1048576)
    maxWebmFilesize = xch.db.Column(xch.db.Integer, unique=False, default=2097152)
    maxMiscFilesize = xch.db.Column(xch.db.Integer, unique=False, default=4194304)
    comlen = xch.db.Column(xch.db.Integer, unique=False, default=2000)
    maxLines = xch.db.Column(xch.db.Integer, unique=False, default=70)
    check_for_block = xch.db.Column(xch.db.Integer, unique=False, default=0)
    clickable_ids = xch.db.Column(xch.db.Integer, unique=False, default=0)
    tag_list = xch.db.Column(xch.db.String, unique=False, default='[]')
    janitor_list = xch.db.Column(xch.db.String, unique=False, default='[]')
    supported_media = xch.db.Column(xch.db.String, unique=False, default='[".jpg", ".jpeg", ".png", ".gif", ".webm", ".mp4"]')

    def __repr__(self):
        return '<Board %r>' % self.title


# class sql_board(xch.db.Model):
#     id = xch.db.Column(xch.db.Integer, primary_key=True)
#     cat = xch.db.Column(xch.db.Integer, primary_key=False)
#     title = xch.db.Column(xch.db.String, unique=True)
#     url = xch.db.Column(xch.db.String, unique=True)
#     description = xch.db.Column(xch.db.String, unique=False)
#     password = xch.db.Column(xch.db.String, unique=False)
#     r9k_mode = xch.db.Column(xch.db.Integer, unique=False)
#     captcha = xch.db.Column(xch.db.Integer, unique=False)
#     nsfw = xch.db.Column(xch.db.Integer, unique=False)
#     post_timeout = xch.db.Column(xch.db.Integer, unique=False)
#     approved = xch.db.Column(xch.db.Integer, unique=False)
#     trip_list = xch.db.Column(xch.db.String, unique=False)
#     supported_media = xch.db.Column(xch.db.String, unique=False)

#     def __repr__(self):
#         return '<Board %r>' % self.title
