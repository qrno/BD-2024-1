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
        "SELECT * FROM post WHERE id_user = ?", (user_id,)
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