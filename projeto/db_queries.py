from flask import (session)

from projeto.db import get_db

def get_all_users():
    db = get_db()
    users = db.execute(
        "SELECT * FROM user"
    ).fetchall()
    return users

def get_user_id():
    return session.get('user_id')