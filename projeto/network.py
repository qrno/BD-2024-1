from flask import (Blueprint, render_template, request, flash, redirect, url_for, session)

from projeto.db import get_db
from projeto.auth import login_required

bp = Blueprint('network', __name__)

@bp.route('/')
def index():
    return render_template('network/index.html')

@bp.route('/user_list')
@login_required
def user_list():
    db = get_db()
    users = db.execute(
        "SELECT * FROM user"
    )
    return render_template('network/user_list.html', users=users)

@bp.route('/create_post', methods=('GET', 'POST'))
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        author_id = session.get('user_id')
        db = get_db()
        error = None

        if not title:
            error = "Title is required"
        if not body:
            error = "Content is required"

        if error is None:
        
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, author_id)
            )
            db.commit()
            
            return redirect(url_for("network.index"))
        
        flash(error)

    return render_template('network/create_post.html')    

@bp.route('/user_post_list')
@login_required
def user_post_list():
    db = get_db()
    user_id = session.get('user_id')
    posts = db.execute(
        "SELECT * FROM post WHERE author_id = ?", (user_id,)
    )
    return render_template('network/user_post_list.html', posts=posts)