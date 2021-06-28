import xch, humanize, os
from xch.models.inject.parse_poster import getMD5
from py_thumbnailer.exceptions import MimeTypeNotFoundException, ThumbnailerNotFoundException
from py_thumbnailer.thumbnail import create_thumbnail
from PIL import Image

def render_file_thumbnail(timestamp, original):
    image_types = [".jpg", ".jpeg", ".jpe", ".gif", ".png", ".bmp"]
    audio_types = [".mp3",".ogg",".wav"]
    video_types = [".webm",".mp4",".avi",".mpg",".mpeg"]
    text_types = [".txt",".pdf",".doc"]
    archive_types = [".zip",".rar",".7z",".tar",".gz"]

    file_path = xch.app.root_path + "/uploads/" + get_file_name(timestamp, original)
    file_path_thumbnail = xch.app.root_path + "/uploads/" + get_file_name(timestamp, original, 1)

    xch.logger.info(file_path)
    xch.logger.info(file_path_thumbnail)

    extension = os.path.splitext(original)[1].lower()
    if extension in image_types:
        xch.logger.info("upload is image type")
        try:
            im = Image.open(file_path)
            if im.mode != 'RGB':
                im = im.convert('RGB')
            im.thumbnail((250,250))
            im.save(file_path_thumbnail, "jpeg")
            return True
        except:
            xch.logger.info("error thumbnailing image (PIL)")
            return False
    else:
        xch.logger.info("upload is other type")
        try:
            xch.logger.info("trying to create thumbnail (py-thumbnailer)")
            preview_buffer = create_thumbnail(file_path, resize_to=250)
        except (ThumbnailerNotFoundException, MimeTypeNotFoundException):
            xch.logger.info("thumbnailer not found (py_thumbnailer)")
            return False
        try:
            xch.logger.info("created thumbnail, attempting to write preview buffer...")
            with open(file_path_thumbnail, 'wb') as fp:
                xch.logger.info("writin preview buffer")
                preview_buffer.seek(0)
                fp.write(preview_buffer.read())
                xch.logger.info("preview buffer written")
            return True
        except:
            xch.logger.info("error writing preview buffer (py_thumbnailer)")
            return False
    xch.logger.info("couldn't render thumbnail (render_file_thumbnail)")
    return False


def get_file_name(timestamp, original, thumbnail=0):
    timestamp = str(timestamp)
    ext = os.path.splitext(original)[1].lower()
    file_numeric = getMD5(original.encode("utf-8"))
    file_numeric = ''.join(c for c in file_numeric if not c.isalpha())[-3:]
    if thumbnail: 
        file_name = timestamp + file_numeric + "s.jpg"
    else:
        file_name = timestamp + file_numeric + ext
    xch.logger.info(str(file_name))
    return file_name

def get_file_info(file_name):
    file_info = {}
    file_info[file_name] = {}
    uploads = xch.app.root_path + "/uploads/"
    file_path = uploads + file_name
    if os.path.isfile(file_path):
        file_md5 = getMD5(open(file_path,'rb').read())
        file_info[file_name]['file_name'] = file_name
        file_info[file_name]['file_time'] = int(os.stat(file_path).st_mtime)
        file_info[file_name]['file_size'] = os.path.getsize(file_path)
        file_info[file_name]['file_size_human'] = humanize.naturalsize(os.path.getsize(file_path))
        file_info[file_name]['file_size_dimensions'] = "800x600"
        file_info[file_name]['file_extension'] = os.path.splitext(file_name)[1].lower()
        file_info[file_name]['file_md5'] = file_md5
    
    return file_info[file_name]