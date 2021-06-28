import xch
from flask import Flask, request, jsonify
from time import strftime
import traceback

import xch.views.index
import xch.views.blotter
import xch.views.category
import xch.views.board
import xch.views.post
import xch.views.thread
import xch.views.file
import xch.views.mod
import xch.views.pages
import xch.views.board_bans
import xch.views.rss
import xch.views.function.post
import xch.views.function.delete
import xch.views.function.board
import xch.views.tripgen

import xch.views.actions
import xch.views.extras

import xch.models.inject.config
import xch.models.inject.title
import xch.models.inject.stats
import xch.models.inject.static_url
import xch.models.inject.render_board_list
import xch.models.inject.render_board_index
import xch.models.inject.render_popular_index
import xch.models.inject.render_stats_index
import xch.models.inject.render_blotter_list
import xch.models.inject.render_thread_list
import xch.models.inject.render_ban_list
import xch.models.inject.render_footer
import xch.models.inject.render_banner

import bs4, functools, htmlmin

def prettify(route_function):
    @functools.wraps(route_function)
    def wrapped(*args, **kwargs):
        yielded_html = route_function(*args, **kwargs)
        soup = bs4.BeautifulSoup(yielded_html, 'html.parser')
        return soup.prettify()

    return wrapped

def uglify(route_function):
    @functools.wraps(route_function)
    def wrapped(*args, **kwargs):
        yielded_html = route_function(*args, **kwargs)
        minified_html = htmlmin.minify(yielded_html)
        return minified_html

    return wrapped

# if xch.app.debug:
#     xch.render_template = prettify(xch.render_template)
# else:
#     xch.render_template = uglify(xch.render_template)

#xch.render_template = uglify(xch.render_template)

xch.db.create_all()

#Run the main app...
if __name__ == '__main__':
    xch.app.run()
