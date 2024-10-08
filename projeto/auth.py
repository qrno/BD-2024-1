from flask import (Blueprint, render_template, request, flash, redirect, url_for, session, g)
from projeto.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        photo = request.files['photo']
        
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif not photo:
            error = "Photo is required"

        if error is None:
            try:
                photo_data = photo.read()
                db.execute(
                    "INSERT INTO user (username, password, photo) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), photo_data)
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = "Username not registered"
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('network.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
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
    return redirect(url_for('network.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("You must be logged in to view this page")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
