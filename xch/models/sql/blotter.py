import xch

def query_blotter(count=0):
    blotter = sql_blotter.query.order_by(sql_blotter.time.desc()).limit(count).all() if count else sql_blotter.query.order_by(sql_blotter.time.desc()).all()
    if blotter:
        xch.logger.info("found blotter items" + str(blotter))
        return blotter
    return []

class sql_blotter(xch.db.Model):
    id = xch.db.Column(xch.db.Integer, primary_key=True)
    content = xch.db.Column(xch.db.String, unique=False)
    time = xch.db.Column(xch.db.Integer, unique=False, default=0)
    posted_by = xch.db.Column(xch.db.String, unique=False)
    
    def __repr__(self):
        return '<Blotter %r>' % self.content