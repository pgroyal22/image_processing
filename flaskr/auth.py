import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
import os

# creates a Blueprint "auth" for authorizing users to upload photos and access uploaded photos
# Blueprint is a group of related Views
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # this is the backend for a user registration form hosted at /auth/register
    # serves template for HTML (in return statement)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # checks if user is already in db    
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        
        # add user to db
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # backend for a login screen hosted at /auth/login
    # also serves template for HTML

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'

        # checks password though secure hash function
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session stores user id so that user's ID follows them after they are logged on
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
            
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    # runs before view so that each time the user id is checked before page is served
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# requires user to login for any view that this function "wraps"
def login_required(view):
    @functools.wraps(view)

    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
            # url_for() generates URL for the view based on the name provided (in this case 'auth.login')
        return view(**kwargs)

    return wrapped_view

