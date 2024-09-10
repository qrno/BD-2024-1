# Quirino

from projeto.db import get_db

def select_group_info(id_group):
    db = get_db()

    group = db.execute(
        'SELECT * FROM `group` WHERE id = ?',
        (id_group,)
    ).fetchone()

    members = db.execute(
        'SELECT * FROM membership WHERE id_group = ?',
        (id_group, )
    ).fetchall()

    posts = select_group_posts(id_group)

    group = dict(group)
    group['members'] = members
    group['posts'] = posts

    print(group)

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

    # posts = db.execute(
    #     'SELECT * FROM post_view WHERE id_user = ?',
    #     (id_user,)
    # ).fetchall()
    #
    # comments = db.execute(
    #     'SELECT * FROM comment_view WHERE id_user = ?',
    #     (id_user,)
    # ).fetchall()

    return user

# Arthur

def get_all_users(db):
    return db.execute(
        "SELECT * FROM user"
    )

def get_all_groups(db):
    return db.execute(
        "SELECT * FROM [group]"
    )

def get_all_memberships(db):
    return db.execute(
        "SELECT * FROM membership"
    )

def get_user_groups(user_id, db):
    return db.execute(
        '''
        SELECT [group].*
        FROM [group]
        JOIN membership m ON [group].id = m.id_group
        WHERE m.id_user = ?
        ''',
        (user_id,)
    )

def get_user_likes(user_id, db):
    return db.execute(
        "SELECT * FROM like WHERE id_user =  ?", 
        (user_id,)
    )

def get_post_likes(post_id, db):
    return db.execute(
        "SELECT * FROM like WHERE id_post = ?",
        (post_id,)
    )

def get_user_posts(user_id, db):
    return db.execute(
        "SELECT * FROM post_view WHERE id_user = ?", (user_id,)
    )

def get_user_comments(user_id, db):
    return db.execute(
        "SELECT * FROM comment WHERE id_user = ?", (user_id,)
    )

def get_user_resposts(user_id, db):
    return db.execute(
        "SELECT * FROM repost WHERE id_user = ?", (user_id,)
    )

def get_post_reposts(post_id, db):
    return db.execute(
        "SELECT * FROM respost WHERE id_post = ?", (post_id,)
    )

def get_user_followers(user_id, db):
    return db.execute(
        "SELECT * FROM follow WHERE id_followed = ?", (user_id,)
    ) 

def get_user_follows(user_id, db):
    return db.execute(
        "SELECT * FROM follow WHERE id_follower = ?", (user_id,)
    )

def get_group(group_id, db):
    return db.execute(
    "SELECT * FROM [group] WHERE id = ?", (group_id,)
    )

def get_group_posts(group_id, db):
    return db.execute(
        "SELECT * FROM post WHERE id_group = ?", (group_id,)
    )

def get_group_members(group_id, db):
    return db.execute(
        '''
        SELECT *
        FROM user
        JOIN membership m ON user.id = m.id_user
        WHERE m.id_group = ? 
        ''',
        (group_id,)
    )

def get_group_id(group_name, db):
    group = db.execute(
        "SELECT * FROM [group] WHERE name = ?", (group_name,)
    ).fetchone()

    if group is not None:
        return group[0]
    return None

def get_chat(user_id1, user_id2, db):
    if int(user_id1) > int(user_id2):
        user_id1 , user_id2 = user_id2 , user_id1

    return db.execute(
        "SELECT * FROM chat WHERE (id_user1 = ? AND id_user2 = ?)",
        (user_id1, user_id2)
    )

def get_chat_id(user_id1, user_id2, db):
    if int(user_id1) > int(user_id2):
        user_id1 , user_id2 = user_id2 , user_id1

    chat = db.execute(
        "SELECT * FROM chat WHERE (id_user1 = ? AND id_user2 = ?)",
        (user_id1, user_id2)
    ).fetchone()

    if chat:
        return chat[0]
    return None

def get_chat_messages(chat_id, db):
    return db.execute(
        "SELECT * FROM message WHERE id_chat = ?",
        (chat_id,)
    )

def insert_chat(user_id1, user_id2, db):
    if int(user_id1) > int(user_id2):
        user_id1, user_id2 = user_id2 , user_id1

    db.execute(
        "INSERT INTO chat (id_user1, id_user2) VALUES (?, ?)",
        (user_id1, user_id2)
    )
    db.commit()

def insert_post(title, body, user_id, group_id, db):
    db.execute(
        "INSERT INTO post (title, body, id_user, id_group) VALUES (?, ?, ?, ?)",
        (title, body, user_id, group_id)
    )
    db.commit()

def insert_group(group_name, db):
    db.execute(
        "INSERT INTO [group] (name) VALUES (?)",
        (group_name,)
    )
    db.commit()

def insert_membership(user_id, group_id, db):
    db.execute(
        "INSERT INTO membership (id_user, id_group) VALUES (?, ?)",
        (user_id, group_id)
    )
    db.commit()

def insert_repost(post_id, user_id, db):
    db.execute(
        "INSERT INTO repost (id_post, id_user) VALUES (?, ?)",
        (post_id, user_id)
    )
    db.commit()

def insert_follow(follower_id, followed_id, db):
    db.execute(
        "INSERT INTO follow (id_follower, id_followed) VALUES (?, ?)",
        (follower_id, followed_id)
    )
    db.commit()

def insert_like(user_id, post_id, db):
    db.execute(
        "INSERT INTO [like] (id_user, id_post) VALUES (?, ?)",
        (user_id, post_id)
    )
    db.commit()

def insert_comment(user_id, post_id, content, db):
    db.execute(
        "INSERT INTO comment (id_user, id_post, content) VALUES (?, ?, ?)",
        (user_id, post_id, content)
    )
    db.commit()

def insert_message(chat_id, user_id, body, db):

    db.execute(
        "INSERT INTO message (id_chat, id_user, body) VALUES (?, ?, ?)",
        (chat_id, user_id, body)
    )
    db.commit()
