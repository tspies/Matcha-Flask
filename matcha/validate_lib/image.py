import re

from flask_uploads          import UploadNotAllowed

from matcha                 import photos
from flask                  import g, flash, session


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def validate_lib_handle_picture_upload(request):
    if request.files:
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                try:
                    image.filename = re.sub(r" ?\([^)]+\)", "", image.filename)
                    photos.save(image)
                    flash('File uploaded', 'success')
                    query_db("INSERT INTO images (username, file_name) VALUES (?,?)",  (session['username'], image.filename))
                    g.db.commit()
                    query_db("UPDATE users SET pics = pics + 1 WHERE username=?", (session['username'],))
                    g.db.commit()
                except UploadNotAllowed:
                    flash('Invalid file upload format', 'danger')
                    return False
            else:
                flash('Uploaded file has an invalid file name', 'danger')
        return False


def validate_lib_update_profile_picture(filename):

    query_db("UPDATE users SET profile_pic=? WHERE username=?", (filename, session['username']))
    g.db.commit()
    flash("Profile Picture Updated, You can now like other users profiles!", 'success')
