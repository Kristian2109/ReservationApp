from datetime import timedelta, date

def is_working_day(day):
    return day.weekday() >= 0 and day.weekday() < 5

def get_next_working_days_strings(current_day, count_next_days):
    days = []
    for i in range(0, count_next_days):
        day = current_day + timedelta(days=i)
        if (is_working_day(day)):
            days.append(day.strftime("%Y/%m/%d"))
    
    return days