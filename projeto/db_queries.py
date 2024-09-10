# Quirino

from projeto.db import get_db

# {{{ Group queries
def select_group_all():
    db = get_db()

    groups = db.execute(
        'SELECT * FROM `group`'
    ).fetchall()

    return groups

def select_group_info(id_group):
    db = get_db()

    group = db.execute(
        'SELECT * FROM `group` WHERE id = ?',
        (id_group,)
    ).fetchone()

    members = db.execute(
        '''
        SELECT user.id, user.username
            FROM membership
                JOIN user ON user.id = membership.id_user
            WHERE membership.id_group = ?
        ''',
        (id_group,)
    ).fetchall()

    posts = select_group_posts(id_group)

    group = dict(group)
    group['members'] = members
    group['posts'] = posts

    return group

def select_group_posts(id_group):
    db = get_db()

    posts = db.execute(
        'SELECT id FROM post_view WHERE id_group = ?',
        (id_group,)
    ).fetchall()
    post_ids = [post['id'] for post in posts]

    posts = []
    for post_id in post_ids:
        posts.append(select_post_info(post_id))

    return posts
# }}}

def select_post_info(id_post):
    db = get_db()

    post = db.execute(
        'SELECT * FROM post_view WHERE id = ?',
        (id_post,)
    ).fetchone()

    comments = db.execute(
        'SELECT * FROM comment_view WHERE id_post = ?',
        (id_post,)
    ).fetchall()

    likes = db.execute(
        'SELECT COUNT(*) from `like` WHERE id_post = ?',
        (id_post,)
    ).fetchone()

    post = dict(post)
    post['comments'] = comments
    post['likes'] = likes['COUNT(*)']

    return post

def select_user_info(id_user):
    db = get_db()

    user = db.execute(
        'SELECT * FROM user WHERE id = ?',
        (id_user,)
    ).fetchone()

    user = dict(user)
    user['groups'] = select_user_groups(id_user)
    user['posts'] = select_user_posts(id_user)

    print(user)

    return user

def select_user_posts(id_group):
    db = get_db()

    posts = db.execute(
        'SELECT id FROM post_view WHERE id_group = ?',
        (id_group,)
    ).fetchall()
    post_ids = [post['id'] for post in posts]

    posts = []
    for post_id in post_ids:
        posts.append(select_post_info(post_id))

    return posts
def select_user_groups(id_user):
    db = get_db()
    groups = db.execute(
        '''
        SELECT * FROM `group`
            JOIN membership ON `group`.id = membership.id_group
            JOIN user ON membership.id_user = user.id
                WHERE user.id = ?
        ''',
        (id_user,)
    ).fetchall()
    return groups

def create_group(name):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO [group] (name) VALUES (?)",
        (name,)
    )
    db.commit()
    return cursor.lastrowid

def create_membership(id_group, id_user):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO membership (id_user, id_group) VALUES (?, ?)",
            (id_user, id_group)
        )
        db.commit()
    except db.IntegrityError:
        return

def create_post(title, body, user_id, group_id):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO post (title, body, id_user, id_group) VALUES (?, ?, ?, ?)",
        (title, body, user_id, group_id)
    )
    db.commit()
    return cursor.lastrowid

def create_follow(id_user, id_follower):
    db = get_db()
    db.execute(
        "INSERT INTO follow (id_user, id_follower) VALUES (?, ?)",
        (id_user, id_follower)
    )
    db.commit()

def create_like(id_user, id_post):
    db = get_db()
    db.execute(
        "INSERT INTO [like] (id_user, id_post) VALUES (?, ?)",
        (id_user, id_post)
    )
    db.commit()

def create_comment(id_user, id_post, content):
    db = get_db()
    db.execute(
        "INSERT INTO comment (id_user, id_post, content) VALUES (?, ?, ?)",
        (id_user, id_post, content)
    )
    db.commit()

def create_message(id_chat, id_user, body):
    db = get_db()
    db.execute(
        "INSERT INTO message (id_chat, id_user, body) VALUES (?, ?, ?)",
        (id_chat, id_user, body)
    )
    db.commit()

# Arthur

def minmax(x, y):
    if x <= y:
        return x, y
    return y, x

def create_chat(id_user1, id_user2):
    id_user1, id_user2 = minmax(id_user1, id_user2)

    db = get_db()
    db.execute(
        "INSERT INTO chat (id_user1, id_user2) VALUES (?, ?)",
        (id_user1, id_user2)
    )
    db.commit()

def select_chat_id(id_user1, id_user2):
    id_user1, id_user2 = minmax(id_user1, id_user2)

    db = get_db()
    chat = db.execute(
        "SELECT * FROM chat WHERE (id_user1 = ? AND id_user2 = ?)",
        (id_user1, id_user2)
    ).fetchone()

    if chat:
        return chat['id']
    return None

def select_chat_messages(chat_id):
    db = get_db()

    messages = db.execute(
        "SELECT * FROM message WHERE id_chat = ?",
        (chat_id,)
    ).fetchall()

    return messages
