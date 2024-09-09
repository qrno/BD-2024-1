from flask import (Blueprint, render_template, request, flash, redirect, url_for, session)

from projeto.db import get_db
from projeto.auth import login_required
from projeto.db_queries import *

bp = Blueprint('network', __name__)

@bp.route('/')
def index():
    return render_template('network/index.html')

@bp.route('/user_list')
@login_required
def user_list():
    users = get_all_users(get_db())
    return render_template('network/user_list.html', users=users)

@bp.route('/group/<id_group>/create_post', methods=('GET', 'POST'))
@login_required
def create_post(id_group):
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        id_user = session.get('user_id')
        db = get_db()
        error = None

        if not title:
            error = "Title is required"
        if not body:
            error = "Content is required"

        if error is None:
            insert_post(title, body, id_user, id_group, db)
            return redirect(url_for("network.group_view", id_group=id_group))
        flash(error)

    return render_template('network/create_post.html')

@bp.route('/user_post_list')
@login_required
def user_post_list():
    db = get_db()
    user_id = session.get('user_id')
    posts = get_user_posts(user_id, db)
    return render_template('network/user_post_list.html', posts=posts)

@bp.route('/create_group', methods=('GET', 'POST'))
@login_required
def create_group():
    if request.method == 'POST':
        name = request.form['name']
        user_id = session.get('user_id')
        db = get_db()
        error = None

        if not name:
            error = "Group name is required"
        if error is None:
            try:
                insert_group(name, db)

                group_id = db.execute(
                    "SELECT * FROM [group] WHERE name = ?", (name,)
                ).fetchone()[0]

                group_id = get_group_id(name, db)

                insert_membership(user_id, group_id, db)
                
            except db.IntegrityError:
                error = f"Group {name} already exists"
            else:
                return redirect(url_for("network.group_view", id_group=group_id))

        flash(error)

    return render_template('network/create_group.html')

@bp.route('/group_list')
@login_required
def group_list():
    db = get_db()
    groups = get_all_groups(db)
    return render_template('network/group_list.html', groups=groups)

@bp.route('/group_view/<id_group>')
def group_view(id_group):
    db  = get_db()

    group = get_group(id_group, db).fetchone()

    posts = get_group_posts(id_group, db).fetchall()
    
    members = get_group_members(id_group, db).fetchall()

    return render_template('network/group_view.html', group=group, posts=posts, members=members)

@bp.route('/user_group_list')
@login_required
def user_group_list():
    db = get_db()
    user_id = session.get('user_id')

    groups = get_user_groups(user_id, db)

    return render_template('network/user_group_list.html', groups=groups)
