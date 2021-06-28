import xch

def query_staff(trip=None):
    options = sql_mods.query.filter_by(trip=trip).first()
    if options:
        xch.logger.info(str(options))
        return options
    return False

class sql_mods(xch.db.Model):
    id = xch.db.Column(xch.db.Integer, primary_key=True)
    rank = xch.db.Column(xch.db.Integer, primary_key=False)
    name = xch.db.Column(xch.db.String, primary_key=False)
    trip = xch.db.Column(xch.db.String, primary_key=False)

    def __repr__(self):
        return '<Staff %r>' % self.name