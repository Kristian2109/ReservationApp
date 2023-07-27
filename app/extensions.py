from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask import flash, redirect, url_for

from flask_login import LoginManager
login_manager = LoginManager()
@login_manager.unauthorized_handler
def unauthorized():
    flash("You aren't authenticated", category="warning")
    return redirect(url_for("main.home"))
login_manager.login_view = "auth.login"

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_admin import Admin
admin = Admin()