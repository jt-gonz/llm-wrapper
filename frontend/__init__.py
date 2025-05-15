from os import path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "llm_db.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "testing_key"  # Cookies?. Add in .env
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import Administrator, Class, Professor, Student, Student_Class

    with app.app_context():
        create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Student.query.get(int(id))

    return app


def create_database(app):
    with app.app_context():
        if not path.exists("frontend/" + DB_NAME):
            db.create_all()
            print("Created Database!")
