from flask import (Blueprint, render_template, request, flash, redirect, url_for, session)

from projeto.db import get_db
from projeto.auth import login_required
from projeto.db_queries import *
import projeto.db_queries as q

bp = Blueprint('network', __name__)

@bp.route('/dev')
def dev():
    return render_template('network/dev.html')

@bp.route('/')
def index():
    return render_template('network/index.html')

@bp.route('/user/<id_user>')
def user_view(id_user):
    user = q.select_user_info(id_user)
    return render_template('network/user_view.html', user=user)

@bp.route('/user_list')
@login_required
def user_list():
    users = get_all_users(get_db())
    return render_template('network/user_list.html', users=users)

@bp.route('/user_post_list')
@login_required
def user_post_list():
    db = get_db()
    user_id = session.get('user_id')
    posts = get_user_posts(user_id, db)
    return render_template('network/user_post_list.html', posts=posts)

@bp.route('/post/<id_post>')
def post(id_post):
    post = q.select_post_info(id_post)
    return render_template('network/post.html', post=post)

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

@bp.route('/group/<id_group>')
def group_view(id_group):
    db  = get_db()

    group = get_group(id_group, db).fetchone()

    print(q.select_group_info(id_group))

    posts = q.select_group_posts(id_group)

    return render_template('network/group_view.html', group=group, posts=posts, members=[])

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


@bp.route('/user_group_list')
@login_required
def user_group_list():
    db = get_db()
    user_id = session.get('user_id')

    groups = get_user_groups(user_id, db)

    return render_template('network/user_group_list.html', groups=groups)

@bp.route('/follow_user/<id_user>', methods=['POST'])
@login_required
def follow_user(id_user):
    db = get_db()
    followed = session.get('user_id')
    error = None
    try:
        insert_follow(followed, id_user, db)
    except db.IntegrityError:
        flash("Already Following")
    
    return render_template('network/user_list.html', users=get_all_users(get_db()))

@bp.route('/like_post/<id_post>', methods=['POST'])
@login_required
def like_post(id_post):
    db = get_db()
    user = session.get('user_id')
    try:
        insert_like(user, id_post, db)
    except db.IntegrityError:
        flash("Already Liked")

    return redirect(request.referrer)

@bp.route('/comment_post/<id_post>', methods=['POST'])
@login_required
def comment_post(id_post):
    db = get_db()
    user = session.get('user_id')
    body = request.form['body']
    if not body:
        flash("Content is required")
    else:
        insert_comment(user, id_post, body, db)
        return redirect(request.referrer or '/')
    return render_template('network/index.html')

@bp.route('/chat/<id_user>', methods=['GET'])
@login_required
def chat(id_user):
    db = get_db()
    current_user = session.get('user_id')

    if current_user == int(id_user):
        flash("Cannot send a message to yourself")
        return redirect(request.referrer or '/')

    chat_id = get_chat_id(int(id_user), int(current_user), db)

    if chat_id:
        messages = get_chat_messages(chat_id, db)
        return render_template('network/chat.html', messages=messages, chat_id=chat_id, other_user_id=id_user)

    return render_template('network/new_chat.html', other_user_id=id_user)

@bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    db = get_db()
    chat_id = request.form['chat_id']
    other_user_id = request.form['other_user_id']
    message_body = request.form['message_body']
    user_id = session.get('user_id')

    insert_message(chat_id, user_id, message_body, db)
    return redirect(url_for('network.chat', id_user=other_user_id)) 

@bp.route('/start_chat/<id_user>', methods=['POST'])
@login_required
def start_chat(id_user):
    db = get_db()
    user_id = session.get('user_id')
    message_body = request.form['message_body']

    insert_chat(user_id, id_user, db)

    chat_id = get_chat_id(user_id, id_user, db)

    insert_message(chat_id, user_id, message_body, db)

    return redirect(url_for('network.chat', id_user=id_user))
