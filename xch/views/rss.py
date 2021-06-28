import xch
from xch.models.sql.board import query_board
from xch.models.sql.post import sql_post, replies_to_post
from xch.models.inject.render_human_time import render_human_time
from xch.models.inject.time import human_date
from xch.models.inject.render_file_info import get_file_info, get_file_name
from xch.models.inject.parse_message import parse_message
from xch.models.inject.slug import get_slug
from flask import make_response

html_escape_table = {
        "'":'&#39;',
        '"':'&quot;',
        '>':'&gt;',
        '<':'&lt;',
        '&':'&amp;'
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

@xch.app.route("/<board>/xml/threads")
def board_xml_threads(board):
    xch.logger.info("accessing " + board + " threads xml feed")
    board_info = query_board(board)
    if board_info:
        activity = []
        activity_item = ""
        count = 0
        limit = 10
        latest_post = 0
        xch.logger.info("thread=0,board="+str(board_info.id)+",limit="+str(limit))
        threads = sql_post.query.filter_by(thread=0).filter_by(board=board_info.id).order_by(sql_post.time.desc()).limit(limit).all()
        xch.logger.info(str(threads))
        for thread in threads:
            activity.append([thread.time, "thread", thread.id])

        activity.sort(reverse=True)
        if len(activity) >= 1:
            latest_post = activity[0][0]

        for item in activity:
            if count < limit:
                if item[1] == "thread":
                    thread = sql_post.query.filter(sql_post.id == item[2]).first()
                    if thread:
                        activity_item += '''<item>
                                            <title>'''+thread.poster+''' created "'''+html_escape(thread.title)+'''" in '''+html_escape(board_info.title)+'''</title>
                                            <link>'''+xch.config['site']['url']+str(board_info.url)+'''/thread/'''+str(thread.id)+'''#p'''+str(thread.id)+'''</link>
                                            <guid isPermalink="false">'''+str(thread.time)+'''</guid>
                                            <pubDate>'''+human_date(thread.time)+'''</pubDate>
                                        </item>'''
                        count += 1
    template = xch.render_template('board_threads.xml', board=board_info, threads=activity_item, latest_thread=latest_post)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response

@xch.app.route("/<board>/xml/posts")
def board_xml_posts(board):
    xch.logger.info("accessing " + board + " posts xml feed")
    board_info = query_board(board)
    if board_info:
        activity = []
        activity_item = ""
        latest_post = 0
        count = 0
        limit = 10
        xch.logger.info("thread!=0,board="+str(board_info.id)+",limit="+str(limit))
        posts = sql_post.query.filter(sql_post.thread != 0).filter_by(board=board_info.id).order_by(sql_post.time.desc()).limit(limit).all()
        xch.logger.info(str(posts))
        for post in posts:
            activity.append([post.time, "post", post.id])

        activity.sort(reverse=True)
        if len(activity) >= 1:
            latest_post = activity[0][0]

        for item in activity:
            if count < limit:
                if item[1] == "post":
                    post = sql_post.query.filter(sql_post.id == item[2]).first()
                    if post:
                        thread = sql_post.query.filter(sql_post.id == post.thread).first()
                        if thread:
                            activity_item += '''<item>
                                                <title>'''+post.poster+''' replied to "'''+html_escape(thread.title)+'''" in '''+html_escape(board_info.title)+'''</title>
                                                <link>'''+xch.config['site']['url']+str(board_info.url)+'''/thread/'''+str(thread.id)+'''#p'''+str(post.id)+'''</link>
                                                <guid isPermalink="false">'''+str(post.time)+'''</guid>
                                                <pubDate>'''+human_date(post.time)+'''</pubDate>
                                            </item>'''
                            count += 1
    template = xch.render_template('board_posts.xml', board=board_info, posts=activity_item, latest_post=latest_post)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response