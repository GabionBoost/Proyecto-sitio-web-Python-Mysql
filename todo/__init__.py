from flask import Flask, render_template
import os #es para interactuar con el sistema operativo

def create_app():  
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY = "mykey",
        DATABASE_HOST = os.environ.get("FLASK_DATABASE_HOST"),
        DATABASE_PASSWORD = os.environ.get("FLASK_DATABASE_PASSWORD"),
        DATABASE_USER = os.environ.get("FLASK_DATABASE_USER"),
        DATABASE = os.environ.get("FLASK_DATABASE")
    )
    
    from . import db
    
    db.init_app(app)
    
    from . import auth
    from . import todo
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)
        
    @app.route("/hola")
    def home():
        return "Hola"
    return app

