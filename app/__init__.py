from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app.extensions import db, login_manager, csrf, bcrypt, admin
from app.models.user import User, UserRole
from app.models.service import Service
from app.models.reservation import ReservationStatus, Reservation

from config import Config

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        return current_user.is_admin() or current_user.is_employee()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    admin.init_app(app)

    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Service, db.session))
    admin.add_view(MyModelView(Reservation, db.session))
    admin.add_view(MyModelView(UserRole, db.session))
    admin.add_view(MyModelView(ReservationStatus, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    # Initialize Flask extensions here
    from app.main import home_blueprint
    from app.auth import auth_blueprint
    from app.reservation import reservation_blueprint
    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(blueprint=reservation_blueprint, url_prefix="/reservation", name="reservation_blueprint")
    # Register blueprints here

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    with app.app_context():
        db.create_all()
    return app