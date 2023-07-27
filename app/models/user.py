from app.extensions import db, bcrypt
from flask_login import UserMixin

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    second_name = db.Column(db.String(length=30), nullable=False)
    phone_number = db.Column(db.String(length=15), nullable=False)
    email_address = db.Column(db.String(length=75), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=256), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("user_role.id"), nullable=False)
    role = db.relationship("UserRole")

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password, rounds=10).decode("utf-8")

    def compare_password(self, password_to_compare):
        return bcrypt.check_password_hash(self.password_hash, password_to_compare)
    
    def is_admin(self):
        return self.role.name == "admin"
    
    def is_employee(self):
        return self.role.name == "employee"