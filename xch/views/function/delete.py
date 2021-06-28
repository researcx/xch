import xch
from xch.models.sql.board import query_board
from xch.models.sql.post import sql_post, replies_in_content
from xch.models.inject.parse_ip import parse_ip
from xch.models.inject.parse_poster import parse_poster
from xch.models.inject.time import unix_time_current
from xch.models.inject.render_file_info import get_file_name
from xch.models.sql.staff import query_staff

@xch.app.route("/<board>/_fn/delete_post", methods=['POST', 'GET'])
def delete_post(board):
    xch.logger.info("attempting to delete post from " + board)
    board_info = query_board(board)
    time_current = unix_time_current()

    if board_info:
        current_ip = parse_ip(xch.request.remote_addr)
        mode = xch.request.args.get('mode')
        pwd = str(xch.request.args.get('pwd'))
        onlyimgdel = True if xch.request.args.get('onlyimgdel') == "on" else False
        query = str(xch.request.args)
        can_delete = False
        count = 0
        if mode == "usrdel":
            can_delete = True
        if can_delete:
            for x, y in xch.request.args.items():
                if y == "delete" and x.isdigit():
                    count = count + 1;
                    postcheck = sql_post.query.filter_by(id=x).first()
                    if postcheck:
                        if ((postcheck.poster_id == current_ip) or (postcheck.poster_ip == current_ip)) or ((postcheck.options == pwd and postcheck.options != "") or (query_staff(parse_poster(pwd)) != False)):
                            if onlyimgdel:
                                file_name = get_file_name(postcheck.time, postcheck.file)
                                thumbnail = get_file_name(postcheck.time, postcheck.file, 1)
                                file_path = xch.app.root_path + "/uploads/" + file_name
                                thumb_path = xch.app.root_path + "/uploads/" + thumbnail
                                if xch.os.path.isfile(file_path): xch.os.remove(file_path)
                                if xch.os.path.isfile(thumb_path): xch.os.remove(thumb_path)
                                postcheck.file = ""
                                xch.db.session.commit()
                                return "File deleted."
                            else:
                                if postcheck.thread == 0:
                                    replies = sql_post.query.filter_by(thread=x).all()
                                    for reply in replies:
                                        file_name = get_file_name(reply.time, reply.file)
                                        thumbnail = get_file_name(reply.time, reply.file, 1)
                                        file_path = xch.app.root_path + "/uploads/" + file_name
                                        thumb_path = xch.app.root_path + "/uploads/" + thumbnail
                                        if xch.os.path.isfile(file_path): xch.os.remove(file_path)
                                        if xch.os.path.isfile(thumb_path): xch.os.remove(thumb_path)
                                        xch.db.session.delete(reply)
                                        xch.db.session.commit()
                                        xch.logger.info(current_ip + " deleted reply " + str(reply.id))
                                file_name = get_file_name(postcheck.time, postcheck.file)
                                thumbnail = get_file_name(postcheck.time, postcheck.file, 1)
                                file_path = xch.app.root_path + "/uploads/" + file_name
                                thumb_path = xch.app.root_path + "/uploads/" + thumbnail
                                if xch.os.path.isfile(file_path): xch.os.remove(file_path)
                                if xch.os.path.isfile(thumb_path): xch.os.remove(thumb_path)
                                xch.db.session.delete(postcheck)
                                xch.db.session.commit()
                                xch.logger.info(current_ip + " deleted post " + str(postcheck.id))
                        else:
                            return "Trying to delete a post that isn't yours."
                    else:
                        return "No such post exists."
            if count > 0:
                return "Deleted " + str(count) + " post(s)"
            else:
                return "No posts were deleted."
    return "Error deleting post."