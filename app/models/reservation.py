from app.extensions import db

class ReservationStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = name = db.Column(db.String(length=30), nullable=False)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_begin = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("reservation_status.id"), nullable=False)
    customer = db.relationship("User", foreign_keys=[customer_id])
    employee = db.relationship("User", foreign_keys=[employee_id])
    service = db.relationship("Service", foreign_keys=[service_id], back_populates="reservations")
    status = db.relationship("ReservationStatus", foreign_keys=[status_id])

#     CREATE TABLE reservations (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     customer_id INT,
#     employee_id INT,
#     service_id INT,
#     time_begin DATETIME,
#     status_id INT,
#     FOREIGN KEY(customer_id) REFERENCES users(id),
#     FOREIGN KEY(employee_id) REFERENCES users(id),
#     FOREIGN KEY(service_id) REFERENCES services(id)
# )