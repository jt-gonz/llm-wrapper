from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import Administrator, Professor, Student

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            flash("Error signing up", category="error")
        else:
            for Model in [Student, Professor, Administrator]:
                user = Model.query.filter_by(email=email).first()
                if user and check_password_hash(user.password, password):
                    flash("Logged in Successfully", category="Success")
                    _ = login_user(user, remember=True)
                    return redirect(url_for("views.home"))

    return render_template("login.html", user=current_user)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    _ = logout_user()
    return redirect(url_for("auth.login"))


# TODO: Differentiate between User permission level.
# TODO: How to confirm that a user is a student at the university?
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
        elif (
            Student.query.filter_by(email=email).first()
            or Professor.query.filter_by(email=email).first()
            or Administrator.query.filter_by(email=email).first()
        ):
            flash("Email already exists", category="error")
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

            login_user(new_student, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)
