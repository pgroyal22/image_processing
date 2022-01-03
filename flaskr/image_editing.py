from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.editing_functions import image_filter
from flaskr.s3upload import upload_file
import os

bp = Blueprint('image_editing', __name__)

ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
PROCESSED_FOLDER='/home/ubuntu/Project1/flaskr/media/processed_photos'  
UNPROCESSED_FOLDER ='/home/ubuntu/Project1/flaskr/media/unprocessed_photos'

@bp.route('/')
@login_required
def index():

    username = g.user['id'] 
    '''
    db = get_db()
    # executes a database command to get all photos by author, sort in desecending order
    edited_images = db.execute(
        'SELECT p.id, filename, created, author_id, username'
        ' FROM photo p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    ''' 
    user_edited_folder = os.path.join(PROCESSED_FOLDER, str (username))
    try:
        photos = os.listdir(user_edited_folder)
    except FileNotFoundError:
        os.mkdir(user_edited_folder)
        photos = os.listdir(user_edited_folder)
    print(photos)
    photos = [file for file in photos]
    return render_template('image_editing/index.html', photos=photos)

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # because of login_required decorator, user needs to be logged into access "create" view
    if request.method == 'POST':
        preset = request.form['preset']
        error = False

        username = str(g.user['id'])

        if 'file' not in request.files:
            flash('No file submitted')
            error = True
        else: 
            file = request.files['file']

        if not preset:
            flash('Preset is required.')
            error = True
        elif file.filename == '':
            flash('No selected file')
            error = True
        
        if error:
             return redirect(request.url)

        if file and allowed_file(file.filename) and not error:

            filename = secure_filename(file.filename)
            file.save(os.path.join(UNPROCESSED_FOLDER, filename)) 
            filename = image_filter(filename, preset, username)
            
            '''
            db = get_db()
            # sends to database
            db.execute(
                'INSERT INTO photo (filename, author_id)'
                ' VALUES (?, ?)',
                (filename, g.user['id'])
            )
            db.commit()
            '''
            upload_file(username, filename) 

            # will redirect to a url that can access uploaded file
            return redirect(url_for('image_editing.uploaded_file',
                                    filename=filename))
        
    return render_template('image_editing/create.html')

@bp.route('/create/<filename>')
@login_required
def uploaded_file(filename):
    path = os.path.join(PROCESSED_FOLDER, str(g.user['id']))
    return send_from_directory(path , filename)
