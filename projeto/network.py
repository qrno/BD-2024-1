from flask import (Blueprint, render_template, request, flash, redirect, url_for, session)

from projeto.db import get_db
from projeto.auth import login_required
import projeto.db_queries as q

bp = Blueprint('network', __name__)

@bp.route('/dev')
def dev():
    return render_template('network/dev.html')

@bp.route('/')
def index():
    id_user = session['user_id']
    user_groups = q.select_user_groups(id_user)
    all_groups = q.select_group_all()
    return render_template('network/index.html', user_groups=user_groups, all_groups=all_groups)

@bp.route('/user/<id_user>')
def user(id_user):
    user = q.select_user_info(id_user)
    return render_template('network/user.html', user=user)

@bp.route('/post/<id_post>')
def post(id_post):
    post = q.select_post_info(id_post)
    return render_template('network/post.html', post=post)

@bp.route('/group/create', methods=('GET', 'POST'))
@login_required
def group_create():
    if request.method == 'POST':
        name = request.form['name']
        user_id = session.get('user_id')

        error = None
        if not name:
            error = "Group name is required"

        if error is None:
            id_group = q.create_group(name)
            q.create_membership(user_id, id_group)
            return redirect(url_for("network.group", id_group=id_group))

        flash(error)

    return render_template('network/group_create.html')

@bp.route('/group/<id_group>')
def group(id_group):
    group = q.select_group_info(id_group)
    return render_template('network/group.html', group=group, posts=group['posts'], members=group['members'])

@bp.route('/group/<id_group>/create_post', methods=('GET', 'POST'))
@login_required
def create_post(id_group):
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        id_user = session.get('user_id')

        error = None
        if not title:
            error = "Title is required"
        if not body:
            error = "Content is required"

        if error is None:
            id_post = q.create_post(title, body, id_user, id_group)
            return redirect(url_for("network.post", id_post=id_post))

        flash(error)

    return render_template('network/create_post.html')

@bp.route('/group/<id_group>/join', methods=['POST'])
@login_required
def join_group(id_group):
    id_user = session.get('user_id')
    q.create_membership(id_group, id_user)
    return redirect(request.referrer)

@bp.route('/follow_user/<id_user>', methods=['POST'])
@login_required
def follow_user(id_user):
    followed = session.get('user_id')
    q.create_follow(followed, id_user)
    return redirect(request.referrer)

@bp.route('/like_post/<id_post>', methods=['POST'])
@login_required
def like_post(id_post):
    user = session.get('user_id')
    q.create_like(user, id_post)
    return redirect(request.referrer)

@bp.route('/comment_post/<id_post>', methods=['POST'])
@login_required
def comment_post(id_post):
    user = session.get('user_id')
    body = request.form['body']
    if not body:
        flash("Content is required")
    else:
        q.create_comment(user, id_post, body)
        return redirect(request.referrer or '/')
    return redirect(url_for('network.post', id_post=id_post))

@bp.route('/chat/<id_user>', methods=['GET'])
@login_required
def chat(id_user):
    current_user = int(session['user_id'])
    id_user = int(id_user)

    if current_user == int(id_user):
        flash("Cannot send a message to yourself")
        return redirect(request.referrer or '/')

    chat_id = q.select_chat_id(id_user, current_user)

    if chat_id:
        messages = q.select_chat_messages(chat_id)
        return render_template('network/chat.html', messages=messages, chat_id=chat_id, other_user_id=id_user)

    return render_template('network/new_chat.html', other_user_id=id_user)

@bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    chat_id = request.form['chat_id']
    message_body = request.form['message_body']

    other_user_id = int(request.form['other_user_id'])
    user_id = int(session['user_id'])

    q.create_message(chat_id, user_id, message_body)
    return redirect(url_for('network.chat', id_user=other_user_id))

@bp.route('/start_chat/<id_user>', methods=['POST'])
@login_required
def start_chat(id_user):
    message_body = request.form['message_body']

    id_user = int(id_user)
    user_id = int(session['user_id'])

    q.create_chat(user_id, id_user)
    chat_id = q.select_chat_id(user_id, id_user)
    q.create_message(chat_id, user_id, message_body)

    return redirect(url_for('network.chat', id_user=id_user))
