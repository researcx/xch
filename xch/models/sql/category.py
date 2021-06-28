import xch

def query_category(category=None):
    options = sql_category.query.filter_by(url=category).first()
    if options:
        xch.logger.info(str(options))
        return options
    return []

class sql_category(xch.db.Model):
    id = xch.db.Column(xch.db.Integer, primary_key=True)
    title = xch.db.Column(xch.db.String, unique=True)
    url = xch.db.Column(xch.db.String, unique=True)
    public = xch.db.Column(xch.db.Integer, unique=False, default=0)
    nsfw = xch.db.Column(xch.db.Integer, unique=False, default=0)
    
    def __repr__(self):
        return '<Category %r>' % self.title