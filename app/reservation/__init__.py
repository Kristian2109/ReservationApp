from flask import Blueprint, flash, redirect, url_for
from flask_login import current_user

reservation_blueprint = Blueprint("reservation", __name__)

@reservation_blueprint.before_request
def is_authenticated_user():
    if current_user.is_anonymous:
        flash("You aren't authenticated", category="warning")
        return redirect(url_for("main.home"))

from app.reservation import routes