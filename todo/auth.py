import functools

from flask import(
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

from werkzeug.security import check_password_hash, generate_password_hash

from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['userName']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'SELECT userID FROM user WHERE userName = %s', (username,)
        )
        if not username:
            error = "Username is null"
        if not password:
            error = "Password is null"    
        elif c.fetchone() is not None:
            error = f"User {username} is register"
        
        if error is None:
            c.execute(
                "INSERT INTO user (userName, password) values(%s,%s)",
                (username, generate_password_hash(password))
            )
            db.commit()
            
            return redirect(url_for("auth.login"))
        flash(error)
    
    return render_template("auth/register.html")
    
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["userName"]
        password = request.form["password"]
        db, c = get_db()
        error = None
        c.execute(
            "SELECT * FROM user WHERE userName = %s", (username,)
        )
        user = c.fetchone()
        if user is None:
            error = "Incorrect"
        elif not check_password_hash( user['password'], password ):
            error = "Incorrect"
            
        if error == None:
            session.clear()
            session["userID"] = user["userID"]
            return redirect(url_for("index"))
        flash(error)
    
    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    userID = session.get("userID")
    if userID is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            "SELECT * FROM user WHERE userID = %s", (userID,)
        )
        g.user = c.fetchone()
 
def login_requerid(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    
    return wrapped_view