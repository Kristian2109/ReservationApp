from app.reservation import reservation_blueprint
from flask import request, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from app.models.service import Service
from app.models.user import User
from app.models.reservation import Reservation
from app.utils.time import get_next_working_days_strings
from datetime import date
from app.extensions import db
from app.utils.reservation import get_free_times_for_reservation
from datetime import timedelta, date, datetime

@reservation_blueprint.route("/choose-service")
@reservation_blueprint.route("/create")
def reserve_service():
    services = Service.query.all()
    return render_template("reservation/chooseServicePage.html", services=services)

@reservation_blueprint.route("/choose-day", methods=["POST"])
def reserve_day():
    service = request.form["service"]
    days = get_next_working_days_strings(date.today(), 7)
    return render_template("reservation/chooseDayPage.html", service=service, days=days)

@reservation_blueprint.route("/choose-time", methods=["POST"])
def reserve_time():
    service = request.form["service"]
    day = request.form["day"]
    service_obj = Service.query.filter_by(name=service).first()

    start_time = timedelta(hours=8)
    end_time = timedelta(hours=17, minutes=30)
    service_duration = timedelta(minutes=service_obj.duration_in_minutes)
    
    formatted_day = day.replace('/', '-')
    reservations = db.session.query(Reservation).filter(Reservation.time_begin.like(f"%{formatted_day}%")).order_by(Reservation.time_begin.asc()).all()
    
    if day == date.today().strftime("%Y/%m/%d"):
        current_time = datetime.now()
        start_time = timedelta(hours=current_time.hour, minutes=current_time.minute + 30 - (current_time.minute % 10))

    reservation_times = get_free_times_for_reservation(start_time, end_time, reservations, service_duration)
    
    formatted_result = [{ "hours": time.seconds // 3600, "minutes": (time.seconds % 3600) // 60 } for time in reservation_times]

    return render_template("reservation/chooseTimePage.html", service=service, day=day, possible_times=formatted_result)

@reservation_blueprint.route("/overview", methods=["POST"])
def reservation_overview():
    service = request.form["service"]
    day = request.form["day"]
    time = request.form["time"]
    print(time)

    service = Service.query.filter_by(name=service).first()
    employee = User.query.filter_by(id=2).first()

    data = {
        "service_name": service.name,
        "service_id": service.id,
        "time": f"{day} {time}",
        "employee_id": employee.id,
        "employee_name": f"{employee.first_name} {employee.second_name}",
        "duration": service.duration_in_minutes,
        "price": service.price_euro
    }
    
    return render_template("reservation/reservationPage.html", data=data)

@reservation_blueprint.route("/", methods=["POST"])
def create_reservation():
    employee_id = request.form["employee_id"]
    customer_id = current_user.id
    service_id = request.form["service_id"]
    reservation_time = request.form["time"]

    new_reservation = Reservation(employee_id=employee_id, customer_id=customer_id, service_id=service_id,
                                  time_begin=reservation_time, status_id = 1)
    
    db.session.add(new_reservation)
    db.session.commit()
    
    return redirect(url_for("main.home"))

@reservation_blueprint.route("/")
def reservations():
    reservations = Reservation.query.filter_by(customer_id=current_user.id).all()

    return render_template("reservation/reservations.html", reservations=reservations)
