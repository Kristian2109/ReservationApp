from datetime import timedelta

def get_timedelta_from_datetime(datetime):
    return timedelta(hours=datetime.hour, minutes=datetime.minute)


def get_free_reservation_times(start_time, end_time, service_duration):

    result = []
    time_tracker = start_time
    last_starting_time = end_time - service_duration

    while time_tracker <= last_starting_time:
        result.append(time_tracker)
        time_tracker += timedelta(minutes=10)

    return result


def get_free_times_for_reservation(start_time, end_time, reservations, service_duration):

    open_starting_time = start_time
    last_possible_starting_time = end_time - service_duration
    reservation_index = 0
    result = []

    while open_starting_time <= last_possible_starting_time:

        if reservation_index >= len(reservations):
            free_current_times = get_free_reservation_times(open_starting_time, end_time, service_duration)
            result.extend(free_current_times)
            break

        current_reservation = reservations[reservation_index]
        starting_time_current_reservation = get_timedelta_from_datetime(current_reservation.time_begin)

        if starting_time_current_reservation - open_starting_time >= service_duration:
            free_current_times = get_free_reservation_times(open_starting_time, starting_time_current_reservation,
                                                            service_duration)
            result.extend(free_current_times)

        open_starting_time = starting_time_current_reservation + timedelta(
            minutes=current_reservation.service.duration_in_minutes)
        reservation_index += 1

    return result