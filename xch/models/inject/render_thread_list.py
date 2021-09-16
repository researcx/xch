import xch
from xch.models.sql.post import sql_post, replies_to_post
from xch.models.sql.board import sql_board
from xch.models.inject.render_human_time import render_human_time
from xch.models.inject.render_file_info import get_file_info, get_file_name
from xch.models.inject.parse_message import parse_message
from xch.models.inject.slug import get_slug
from xch.models.inject.config import get_site_url

#@xch.cache.memoize(timeout=86400) # render_thread_stats
def render_thread_stats(thread):
    is_sticky = ""
    is_closed = ""
    render = ""

    thread = sql_post.query.filter_by(id=thread).first()
    if thread:
        post_count = sql_post.query.filter(sql_post.thread == thread.id).count()

        if thread.is_sticky:
            is_sticky = "Sticky / "
        if thread.is_closed:
            is_closed = "Closed / "


        render = is_sticky + is_closed + '''<span class="ts-replies" data-tip="Replies">'''+str(post_count)+'''</span> / <span class="ts-images" data-tip="Images">IMAGES_NOTIMPLEMENTED</span> / <span data-tip="Posters" class="ts-ips">POSTERS_NOTIMPLEMENTED</span> / <span data-tip="Page" class="ts-page">PAGES_NOTIMPLEMENTED</span>'''

    return render
xch.app.jinja_env.globals.update(render_thread_stats=render_thread_stats)

#@xch.cache.memoize(timeout=86400) # render_thread_list
def render_thread_list(thread_specific=0, thread_count=15, reply_count=4, page=1, stickies=0, board=""):
    render = ""
    disclaimer = ""
    is_sticky = ""
    is_closed = ""
    backlinks = ''
    if xch.config['site']['post_disclaimer_enabled']:
        disclaimer = '<div class="post-disclaimer">'+xch.config['site']['post_disclaimer']+'</div>'
    board = sql_board.query.filter_by(url=board).first()
    if board:
        threads = sql_post.query.filter_by(thread=0).filter_by(is_sticky=0).filter_by(board=board.id).order_by(sql_post.time.desc()).limit(thread_count).all()
        if stickies:
            threads = sql_post.query.filter_by(thread=0).filter_by(is_sticky=1).filter_by(board=board.id).limit(thread_count).all()
        if thread_specific:
            threads = sql_post.query.filter_by(id=thread_specific).limit(thread_count).all()
        if threads:
            xch.logger.info("found threads " + str(threads))
            for thread in threads:
                backlinks = ""
                is_sticky = ""
                is_closed = ""

                for reply in replies_to_post(thread.id, thread.id):
                    backlinks += '<span><a href="#p'+str(reply)+'" class="quotelink">&gt;&gt;'+str(reply)+'</a></span> '
                if thread.is_sticky:
                    is_sticky = '<img src="//s.4cdn.org/image/sticky.gif" alt="Sticky" title="Sticky" class="stickyIcon retina">'
                if thread.is_closed:
                    is_closed = '<img src="//s.4cdn.org/image/closed.gif" alt="Closed" title="Closed" class="closedIcon retina">'
                render += '''
                            <div class="thread" id="t'''+str(thread.id)+'''">
                                <div class="postContainer opContainer" id="pc'''+str(thread.id)+'''">
                                    <div id="p'''+str(thread.id)+'''" class="post op">
                                        <div class="postInfoM mobile" id="pim'''+str(thread.id)+'''"> <span class="nameBlock"><span class="name">'''+thread.title+'''</span> '''+is_sticky+''' '''+is_closed+'''<br/><span class="subject"><span data-tip=""
                                                        data-tip-cb="mShowFull">'''+thread.content+'''</span></span> </span><span class="dateTime postNum"
                                                data-utc="'''+str(thread.time)+'''">'''+render_human_time(thread.time)+''' <a href="'''+get_site_url()+board.url+'''/thread/'''+str(thread.id)+'''#p'''+str(thread.id)+'''"
                                                    title="Link to this post">No.</a><a href="'''+get_site_url()+board.url+'''/thread/'''+str(thread.id)+'''#q'''+str(thread.id)+'''"
                                                    title="Reply to this post">'''+str(thread.id)+'''</a></span></div>'''
                if 'file_size_human' in get_file_info(get_file_name(thread.time, thread.file)):
                    render += '''
                                        <div class="file" id="f'''+str(thread.id)+'''">
                                            <div class="fileText" id="fT'''+str(thread.id)+'''">File: <a href="'''+get_site_url()+board.url+'''/'''+get_file_name(thread.time, thread.file)+'''"
                                                    target="_blank">'''+thread.file+'''</a> ('''+get_file_info(get_file_name(thread.time, thread.file))['file_size_human']+''', '''+get_file_info(get_file_name(thread.time, thread.file))['file_size_dimensions']+''')</div><a class="fileThumb"
                                                href="'''+get_site_url()+board.url+'''/'''+get_file_name(thread.time, thread.file)+'''" target="_blank"><img
                                                    src="'''+get_site_url()+board.url+'''/'''+get_file_name(thread.time, thread.file, thumbnail=1)+'''" alt="'''+get_file_info(get_file_name(thread.time, thread.file))['file_size_human']+'''" data-md5="'''+get_file_info(get_file_name(thread.time, thread.file))['file_md5']+'''"
                                                    style="height: auto; width: auto; max-height: 250px; max-width:250px;" loading="lazy">
                                                <div data-tip="" data-tip-cb="mShowFull" class="mFileInfo mobile">'''+get_file_info(get_file_name(thread.time, thread.file))['file_size_human']+''' '''+get_file_info(get_file_name(thread.time, thread.file))['file_extension']+'''</div>
                                            </a>
                                        </div>'''
                render += '''
                                        <div class="postInfo desktop" id="pi'''+str(thread.id)+'''"><input type="checkbox" name="'''+str(thread.id)+'''" value="delete"> <span
                                                class="subject">'''+thread.title+'''</span> <span class="nameBlock"><span
                                                    class="name">'''+thread.poster+'''</span></span> '''
                if board.show_location:
                    render += '''<img class="flag flag-us" src="'''+get_site_url()+'''_rsc/icon/flag/'''+thread.poster_location+'''.gif" style="margin: -2px 0;" alt="['''+thread.poster_location+''']" title="'''+thread.poster_location+'''" /> '''
                    
                render += '''<span class="dateTime"
                                                data-utc="'''+str(thread.time)+'''">'''+render_human_time(thread.time)+'''</span> <span class="postNum desktop"><a
                                                    href="'''+get_site_url()+board.url+'''/thread/'''+str(thread.id)+'''#p'''+str(thread.id)+'''" title="Link to this post">No.</a><a
                                                    href="'''+get_site_url()+board.url+'''/thread/'''+str(thread.id)+'''#q'''+str(thread.id)+'''" title="Reply to this post">'''+str(thread.id)+'''</a> '''+is_sticky+''' '''+is_closed+'''
                                                &nbsp; <span>[<a href="'''+get_site_url()+board.url+'''/thread/'''+str(thread.id)+'''/'''+get_slug(thread.title)+'''"
                                                        class="replylink">Reply</a>]</span></span>
                                                        <div id="bl_'''+str(thread.id)+'''" class="backlink">'''+backlinks+'''</div>
                                                        </div>'''
                render += '''
                                        <blockquote class="postMessage" id="m'''+str(thread.id)+'''">'''+parse_message(thread.content)+'''</blockquote>
                                        '''+disclaimer+'''
                                    </div>
                                    <div class="postLink mobile"><span class="info">4 Replies / 3 Images</span><a href="'''+get_site_url()+board.url+'''/thread/'''+str(thread.id)+'''"
                                            class="button">View Thread</a></div>
                                </div>'''
                if not thread_specific:
                    replies = sql_post.query.filter_by(thread=thread.id).order_by(sql_post.time.desc()).limit(reply_count).all()
                else:
                    replies = sql_post.query.filter_by(thread=thread.id).limit(reply_count).all()
                for post in replies:
                    backlinks = ""
                    for reply in replies_to_post(post.id, post.thread):
                        backlinks += '<span><a href="#p'+str(reply)+'" class="quotelink">&gt;&gt;'+str(reply)+'</a></span> '
                #render += '''<span class="summary desktop">3 replies and 2 images omitted. <a href="'''+get_site_url()+board.url+'''/thread/'''+str(thread.id)+'''" class="replylink">Click here</a> to view.</span>'''
                    render += '''<div class="postContainer replyContainer" id="pc'''+str(post.id)+'''">
                                    <div class="sideArrows" id="sa'''+str(post.id)+'''">&gt;&gt;</div>
                                    <div id="p'''+str(post.id)+'''" class="post reply">
                                        <div class="postInfoM mobile" id="pim'''+str(post.id)+'''"> <span class="nameBlock"><span class="name">'''+post.poster+'''</span> <br/></span><span class="dateTime postNum"
                                                data-utc="'''+str(post.time)+'''">'''+render_human_time(post.time)+''' <a href="'''+get_site_url()+board.url+'''/thread/'''+str(thread.id)+'''#p'''+str(post.id)+'''"
                                                    title="Link to this post">No.</a><a href="'''+get_site_url()+board.url+'''/thread/'''+str(thread.id)+'''#q'''+str(post.id)+'''"
                                                    title="Reply to this post">'''+str(post.id)+'''</a></span></div>
                                        <div class="postInfo desktop" id="pi'''+str(post.id)+'''"><input type="checkbox" name="'''+str(post.id)+'''" value="delete"> <span
                                                class="subject">'''+post.title+'''</span> <span
                                                class="nameBlock"><span class="name">'''+post.poster+'''</span></span> '''
                    if board.show_location:
                        render += '''<img class="flag flag-us" src="'''+get_site_url()+'''_rsc/icon/flag/'''+post.poster_location+'''.gif" style="margin: -2px 0;" alt="['''+post.poster_location+''']" title="'''+post.poster_location+'''" /> '''

                    render += '''<span class="dateTime" data-utc="'''+str(post.time)+'''">'''+render_human_time(post.time)+'''</span> <span
                                                class="postNum desktop"><a href="'''+get_site_url()+board.url+'''/thread/'''+str(thread.id)+'''#p'''+str(post.id)+'''" title="Link to this post">No.</a><a
                                                    href="'''+get_site_url()+board.url+'''/thread/'''+str(thread.id)+'''#q'''+str(post.id)+'''" title="Reply to this post">'''+str(post.id)+'''</a></span>
                                                    <div id="bl_'''+str(post.id)+'''" class="backlink">'''+backlinks+'''</div>
                                                    </div>'''
                    if 'file_size_human' in get_file_info(get_file_name(post.time, post.file)):
                        render += '''<div class="file" id="f'''+str(post.id)+'''">
                                                <div class="fileText" id="fT'''+str(post.id)+'''">File: <a href="'''+get_site_url()+board.url+'''/'''+get_file_name(post.time, post.file)+'''"
                                                        target="_blank">'''+post.file+'''</a> ('''+get_file_info(get_file_name(post.time, post.file))['file_size_human']+''', '''+get_file_info(get_file_name(post.time, post.file))['file_size_dimensions']+''')</div><a class="fileThumb"
                                                    href="'''+get_site_url()+board.url+'''/'''+get_file_name(post.time, post.file)+'''" target="_blank"><img
                                                        src="'''+get_site_url()+board.url+'''/'''+get_file_name(post.time, post.file, thumbnail=1)+'''" alt="'''+get_file_info(get_file_name(post.time, post.file))['file_size_human']+'''" data-md5="'''+get_file_info(get_file_name(post.time, post.file))['file_md5']+'''"
                                                        style="height: auto; width: auto; max-height: 250px; max-width:250px;" loading="lazy">
                                                    <div data-tip="" data-tip-cb="mShowFull" class="mFileInfo mobile">'''+get_file_info(get_file_name(post.time, post.file))['file_size_human']+''' PNG</div>
                                                </a>
                                            </div>'''
                    render += '''<blockquote class="postMessage" id="m'''+str(post.id)+'''">'''+parse_message(post.content)+'''</blockquote>
                    '''+disclaimer+'''
                                    </div>
                                </div>'''
                render += '</div><hr>'

    return render
xch.app.jinja_env.globals.update(render_thread_list=render_thread_list)