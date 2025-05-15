from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import Student

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    data = request.form
    print(data)
    return render_template("login.html")


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    return "<p>Logout</p>"


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form
        first_name = data.get("first-name")
        last_name = data.get("last-name")
        email = data.get("email")
        password = data.get("password")
        password_confirmation = data.get("password-confirmation")

        if (
            not first_name
            or not last_name
            or not email
            or not password
            or not password_confirmation
        ):
            flash("Error signing up", category="error")
        elif password != password_confirmation:
            flash("Passwords don't match", category="error")
        else:
            hash_password = generate_password_hash(password)
            new_student = Student(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hash_password,
                credits=5000,
            )
            db.session.add(new_student)
            db.session.commit()

            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html")
