from os import path

from flask import Flask
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

    create_database(app)

    return app


def create_database(app):
    with app.app_context():
        if not path.exists("frontend/" + DB_NAME):
            db.create_all()
            print("Created Database!")
