from flask import(
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from werkzeug.exceptions import abort
from todo.auth import login_requerid
from todo.db import get_db

bp = Blueprint("todo", __name__)

@bp.route("/")
@login_requerid
def index():
    db, c = get_db()
    c.execute(
        "SELECT t.todoID, t.description, u.userName, t.completed, t.create_at from todo t JOIN user u ON t.userID = u.userID order by create_at desc"
    )
    todos = c.fetchall()
    return render_template("todo/index.html", todos=todos )