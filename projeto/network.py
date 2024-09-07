from flask import (Blueprint, render_template)

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
