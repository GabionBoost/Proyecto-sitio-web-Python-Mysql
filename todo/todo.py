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
        "SELECT t.todoID, t.description, u.userName, t.completed, t.create_at from todo t JOIN user u ON t.userID = u.userID WHERE t.userID = %s order by create_at desc;",
        (g.user["userID"],)
    )
    todos = c.fetchall()
    return render_template("todo/index.html", todos=todos )

@bp.route("/create", methods=['GET', 'POST'])
@login_requerid
def create():
    if request.method == "POST":
        description = request.form["description"]
        error = None
        if not description:
            error = "Description is required"
        elif error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                "INSERT INTO todo (description, completed, userID) VALUES(%s,%s,%s);",
                (description, False, g.user["userID"])
            ) 
            db.commit()
            return redirect(url_for("todo.index"))
    return render_template("todo/create.html")

def get_todo(id):
    db, c = get_db()
    c.execute(
        "SELECT t.todoID, t.description, t.completed, t.userID, t.create_at, u.userName FROM todo t JOIN user u ON t.userID = u.userID WHERE t.todoID = %s;",
        (id,)
    )
    
    todo = c.fetchone()
    if todo is None:
        abort(404, f"The id of todo {id} does'nt exist")

    return todo
    
@bp.route("/<int:id>/update", methods=['GET', 'POST'])
@login_requerid
def update(id):
    todo = get_todo(id)
    
    if request.method == "POST":
        description = request.form["description"]
        completed = True if request.form["completed"] == "on" else False
        error = None
        
        if not description:
            error = "Description is required"
            
        elif error is not None:
            flash(error)
            
        else:
            db, c = get_db()
            c.execute(
               'UPDATE todo SET description = %s, completed = %s WHERE todoID = %s AND userID = %s;', (description, completed, id, g.user["userID"])
               )
            db.commit()
            return redirect(url_for("todo.index"))
            
    return render_template("todo/update.html", todo=todo)

@bp.route("/<int:id>/delete", methods=['POST'])
@login_requerid
def delete(id):
    db, c = get_db()
    c.execute("DELETE FROM todo WHERE todoID = %s AND userID = %s;", (id, g.user["userID"]))
    db.commit()
    return redirect(url_for("todo.index"))