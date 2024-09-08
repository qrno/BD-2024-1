def get_all_users():
    users = db.execute(

    ).fetchall()
    return users
