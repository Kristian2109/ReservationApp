from app.main import home_blueprint
from flask import render_template

@home_blueprint.route("/home")
@home_blueprint.route("/")
def home():
    return render_template("main.html")