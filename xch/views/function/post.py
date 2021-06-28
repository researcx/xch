import xch
from xch.models.sql.board import query_board
from xch.models.inject.render_ban_list import render_ban_list
from xch.models.inject.parse_ip import parse_ip, country_from_ip
from xch.models.inject.parse_poster import parse_poster
from xch.models.sql.post import sql_post, replies_in_content
from xch.models.inject.time import unix_time_current
from xch.models.inject.render_file_info import get_file_name, render_file_thumbnail
from werkzeug.utils import secure_filename

@xch.app.route("/<board>/_fn/create_post", methods=['POST', 'GET'])
def create_post(board):
    xch.logger.info("attempting to post in " + board)
    board_info = query_board(board)
    time_current = unix_time_current()
    upfile = ""

    if board_info:
        if board_info.captcha and xch.config['hcaptcha']['enabled']:
            if not xch.hcaptcha.verify():
                return "Captcha verification failed."

        # max_file_size = xch.request.form['MAX_FILE_SIZE']
        mode = xch.request.form['mode']
        pwd = xch.request.form['pwd']
        file_name = ""
    
        poster = parse_poster(xch.request.form['name'])
        poster_id = parse_ip(xch.request.remote_addr)
        poster_ip = parse_ip(xch.request.remote_addr)
        options = xch.request.form['email']
        title = xch.request.form['sub']
        content = xch.request.form['com']
        thread = int(xch.request.form['thread']) if 'thread' in xch.request.form else 0

        replies = str(replies_in_content(content)) if replies_in_content(content) else "[]"

        if board_info.show_location:
            poster_location = country_from_ip(xch.request.remote_addr)['iso_code'].lower()
        else:
            poster_location = "un"

        if thread == 0 and title == "":
            return "No title specified."

        if thread == 0:
            if 'upfile' not in xch.request.files:
                return "No file selected."
        upfile = xch.request.files['upfile']
        if upfile.filename == '':
            return "No file selected."
        if upfile:
            
            file_name = secure_filename(upfile.filename)
            file_path = xch.app.root_path + "/uploads/" + get_file_name(time_current, file_name) 
        
            extension = xch.os.path.splitext(file_name)[1].lower()
            if extension not in board_info.supported_media:
                return "Invalid file type."

            upfile.save(file_path)
            try:
                can_thumbnail = render_file_thumbnail(time_current, file_name)
                if can_thumbnail == False:
                    return "Error creating thumbnail."
            except:
                return "Error creating thumbnail."
        new_post = sql_post(time=time_current, content=content, title=title, poster=poster, poster_id=poster_id, poster_ip=poster_ip, poster_location=poster_location, file=file_name, options=options, board=board_info.id, thread=thread, reply_to=replies, is_sticky=0, is_closed=0, is_archived=0)
        xch.db.session.add(new_post)
        xch.db.session.flush()
        post_id = str(new_post.id)
        xch.db.session.commit()

        if thread == 0:
            return xch.redirect('/'+board_info.url+'/thread/'+str(post_id))
        else:
            return xch.redirect('/'+board_info.url+'/thread/'+str(thread)+'#p'+str(post_id))