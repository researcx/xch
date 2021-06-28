import xch


class sql_bans(xch.db.Model):
    id = xch.db.Column(xch.db.Integer, primary_key=True)
    user = xch.db.Column(xch.db.String, unique=False)
    reason = xch.db.Column(xch.db.String, unique=False)
    board = xch.db.Column(xch.db.String, unique=False)
    length = xch.db.Column(xch.db.Integer, unique=False, default=0)
    time = xch.db.Column(xch.db.Integer, unique=False, default=0)
    expires = xch.db.Column(xch.db.Integer, unique=False, default=0)
    post = xch.db.Column(xch.db.Integer, unique=False)
    moderator = xch.db.Column(xch.db.String, unique=False)
    display = xch.db.Column(xch.db.Integer, unique=False, default=0)

def __repr__(self):
    return '<Banned %r>' % self.user