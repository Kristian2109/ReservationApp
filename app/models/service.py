from app.extensions import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(length=512), nullable=False)
    duration_in_minutes = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    price_euro = db.Column(db.Integer)
    reservations=db.Relationship("Reservation")

# CREATE TABLE services (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(30),
#     description VARCHAR(512),
#     duration_in_minutes INT,
#     CHECK (duration_in_minutes <= 180 AND duration_in_minutes > 0)
# );