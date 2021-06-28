import xch
from xch.models.sql.category import sql_category
from xch.models.sql.board import sql_board

									# <div class="c-thread">
									# 	<div class="c-board">Television &amp; Film</div><a
									# 		href="/tv/thread/148493243" class="boardlink"><img alt=""
									# 			class="c-thumb" src="//i.4cdn.org/tv/1616536109548s.jpg" width="100"
									# 			height="150"></a>
									# 	<div class="c-teaser">Was this any good?</div>
									# </div>

#@xch.cache.memoize(timeout=86400) # render_popular_index
def render_popular_index(nsfw=0):
    render = ""
    rendered_threads = []
    boards = sql_board.query.filter_by(nsfw=nsfw).all()
    xch.logger.info(str(boards))
    for board in boards:
        return ""

        render = '''
                <div class="c-thread">
                    <div class="c-board">\'''+board.title+\'''</div><a
                        href="/tv/thread/148493243" class="boardlink"><img alt=""
                            class="c-thumb" src="//i.4cdn.org/tv/1616536109548s.jpg" width="100"
                            height="150"></a>
                    <div class="c-teaser">Was this any good?</div>
                </div>'''
    return render

xch.app.jinja_env.globals.update(render_popular_index=render_popular_index)
