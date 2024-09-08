from flask import (session)

from projeto.db import get_db

def get_all_users(db=get_db()):
    return db.execute(
        "SELECT * FROM user"
    )

def get_all_groups(db=get_db()):
    return db.execute(
        "SELECT * FROM group"
    )

def get_user_likes(user_id, db=get_db()):
    return db.execute(
        "SELECT * FROM like WHERE id_user =  ?", 
        (user_id,)
    )

def get_post_likes(post_id, db=get_db()):
    return db.execute(
        "SELECT * FROM like WHERE id_post = ?",
        (post_id,)
    )

def get_user_posts(user_id, db=get_db()):
    return db.execute(
        "SELECT * FROM post WHERE id_user = ?", (user_id,)
    )

def get_user_comments(user_id, db=get_db()):
    return db.execute(
        "SELECT * FROM comment WHERE id_user = ?", (user_id,)
    )

def get_user_resposts(user_id, db=get_db()):
    return db.execute(
        "SELECT * FROM repost WHERE id_user = ?", (user_id,)
    )

def get_post_reposts(post_id, db=get_db()):
    return db.execute(
        "SELECT * FROM respost WHERE id_post = ?", (post_id,)
    )

def get_user_followers(user_id, db=get_db()):
    return db.execute(
        "SELECT * FROM follow WHERE id_followed = ?", (user_id,)
    ) 

def get_user_follows(user_id, db=get_db()):
    return db.execute(
        "SELECT * FROM follow WHERE id_follower = ?", (user_id,)
    )

def get_group(group_name, db=get_db()):
    return db.execute(
    "SELECT * FROM [group] WHERE name = ?", (group_name,)
    )

def get_group_id(group_name, db=get_db()):
    group = db.execute(
        "SELECT * FROM [group] WHERE name = ?", (group_name,)
    ).fetchone()

    if group is not None:
        return group[0]
    return None


def insert_post(title, body, user_id, group_id, db=get_db()):
    db.execute(
        "INSERT INTO post (title, body, id_user, id_group) VALUES (?, ?, ?, ?)",
        (title, body, user_id, group_id)
    )
    db.commit()

def insert_group(group_name, db=get_db()):
    db.execute(
        "INSERT INTO [group] (name) VALUES (?)",
        (group_name,)
    )
    db.commit()

def insert_membership(user_id, group_id, db=get_db()):
    db.execute(
        "INSERT INTO membership (id_user, id_group) VALUES (?, ?)",
        (user_id, group_id)
    )
    db.commit()

def insert_repost(post_id, user_id, db=get_db()):
    db.execute(
        "INSERT INTO repost (id_post, id_user) VALUES (?, ?)",
        (post_id, user_id)
    )
    db.commit()

def insert_follow(follower_id, followed_id, db=get_db()):
    db.execute(
        "INSERT INTO follow (id_follower, id_followed) VALUES (?, ?)",
        (follower_id, followed_id)
    )
    db.commit()

def insert_like(user_id, post_id, db=get_db()):
    db.execute(
        "INSERT INTO [like] (id_user, id_post) VALUES (?, ?)",
        (user_id, post_id)
    )
    db.commit()

def insert_comment(user_id, post_id, content, db=get_db()):
    db.execute(
        "INSERT INTO comment (id_user, id_post, content) VALUES (?, ?, ?)",
        (user_id, post_id, content)
    )
    db.commit()

def insert_chat(user_id1, user_id2, db=get_db()):
    db.execute(
        "INSERT INTO chat (id_user1, id_user2) VALUES (?, ?)",
        (user_id1, user_id2)
    )
    db.commit()

def insert_message(chat_id, user_id, body, db=get_db()):
    db.execute(
        "INSERT INTO message (id_chat, id_user, body) VALUES (?, ?, ?)",
        (chat_id, user_id, body)
    )
    db.commit()