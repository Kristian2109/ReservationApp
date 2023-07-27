from flask import render_template, request, redirect, url_for, flash
from app.auth import auth_blueprint
from app.models.user import User
from app.extensions import db, bcrypt, login_manager
from flask_login import login_user, current_user, logout_user

@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You have already logged in!", category="warning")
        return redirect(url_for("main.home"))
    
    if request.method == "POST":
        form_data = request.form
        if form_data["password1"] != form_data["password2"]:
            flash("Passwords are different!", category="warning")
            return redirect(url_for("auth.register"))

        registered_user = User.query.filter_by(email_address=form_data["email"]).first()
        if registered_user:
            flash("User already registered with this email!", category="warning")
            return redirect(url_for("auth.register"))
        
        new_user = User(first_name=form_data["first_name"], second_name=form_data["second_name"], 
                        email_address=form_data["email"], password=form_data["password1"], \
                        phone_number=form_data["phone_number"], is_active=True,
                        role_id=1)
        
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("main.home"))

    return render_template("auth/register.html")

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You have already logged in!", category="warning")
        return redirect(url_for("main.home"))
    
    if request.method == "POST":
        form_data = request.form
        user = User.query.filter_by(email_address=form_data["email"]).first()
        if not user:
            flash("False email address", category="warning")
            return redirect(url_for("auth.login"))
        
        if not user.compare_password(form_data["password"]):
            flash("False password!", category="warning")
            return redirect(url_for("auth.login"))
        
        else:
            remember = True if form_data.get("remember") else False
            login_user(user, remember=remember)
            print(form_data)
            print(remember)
            flash("You've successfully logged in!", category="success")
            return redirect(url_for("main.home"))

    return render_template("auth/login.html")

@auth_blueprint.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("main.home"))