import xch, piexif, random, string # base64, hashlib
from werkzeug.utils import secure_filename

#upload file
@xch.app.route("/d", methods=['GET', 'POST'])
def do_upload():
    if xch.request.method == 'POST':
        timer = int(xch.request.form['timer']) if 'timer' in xch.request.form else 0
        timer_code = "0"
        encoded_string = ""

        allowed_times = [1, 5, 10, 0]
        exif_types = [".jpg", ".jpeg", ".jpe"]
        other_image_types = [".png", ".bmp", ".webp", ".gif"]

        upload_folder = xch.app.static_folder + "/data/uploads/"
        if not xch.os.path.exists(upload_folder):
            xch.os.makedirs(upload_folder)

        if timer not in allowed_times:
            xch.flash('invalid timer setting.', 'danger')
            return xch.redirect('/u')
        else:
            timer_code = str(timer)
        if 'file' not in xch.request.files:
            xch.flash('no image selected.', 'danger')
            return xch.redirect('/u')
        file = xch.request.files['file']
        if file.filename == '':
            xch.flash('no image selected.', 'danger')
            return xch.redirect('/u')
        if file:
            file_name = secure_filename(file.filename)
            extension = xch.os.path.splitext(file_name)[1]
            new_name = ''.join(random.sample("-_"+string.ascii_uppercase+string.ascii_lowercase+string.digits,20)) + extension
            new_name = timer_code + '.' + new_name
            file.save(xch.os.path.join(upload_folder, new_name))
            #with open(upload_folder+new_name, "rb") as image_file:
            #    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")[0:16]
            #    hashname = hashlib.sha256(encoded_string.encode()).hexdigest()[-8:]
            if extension in exif_types:
                piexif.remove(upload_folder + new_name)
                #xch.flash('link: <a href="/v/'+hashname+'/'+new_name+'#'+encoded_string+'">/v/'+hashname+'/'+new_name+'#'+encoded_string+'</a> (will self-destruct upon visiting)', 'success')
                xch.flash('link: <a href="/v/'+new_name+'">/v/'+new_name+'</a> (will self-destruct upon visiting)', 'success')
                return xch.redirect('/u')
            elif extension in other_image_types:
                #xch.flash('link: <a href="/v/'+hashname+'/'+new_name+'#'+encoded_string+'">/v/'+hashname+'/'+new_name+'#'+encoded_string+'</a> (will self-destruct upon visiting)', 'success')
                xch.flash('link: <a href="/v/'+new_name+'">/v/'+new_name+'</a> (will self-destruct upon visiting)', 'success')
                return xch.redirect('/u')
            else:
                xch.flash('invalid image type.', 'danger')
                xch.os.system("shred -u "+upload_folder + new_name)
                return xch.redirect('/u')
        else:
            xch.flash('invalid image.', 'danger')
            return xch.redirect('/u')
    xch.flash('no image selected.', 'danger')
    return xch.redirect('/u')