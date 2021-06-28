import xch
from xch.models.sql.category import sql_category
from xch.models.sql.board import sql_board

@xch.app.route("/create")
def create_board():
    categories = sql_category.query.filter_by(public=1).all()
    category_list = []
    for cat in categories:
        category_list.append([cat.title, " "])

    return xch.render_template('create_board.html', page_title="Create a new board", boards=category_list)

#http://0.0.0.0:5000/_fn/post?uri=xch
# title=research
# subtitle=fags
# username=keira%23niggers
# shared_secret=lol

@xch.app.route("/_fn/create_board", methods=['GET', 'POST'])
def fn_create_board():
    uri = xch.request.args.get('uri')
    title = xch.request.args.get('title')
    subtitle = xch.request.args.get('subtitle')
    username = xch.request.args.get('username')
    shared_secret = xch.request.args.get('shared_secret')

    xch.logger.info("attempting to create a board called " + title)
    new_board = sql_board(cat=0, title=title, url=uri, description=subtitle, password=shared_secret, owned_by=username)
    xch.db.session.add(new_board)
    xch.db.session.flush()
    xch.db.session.commit()

    print(str(xch.request.args))
    return(str(xch.request.args))
    #return '/'+board+'/'