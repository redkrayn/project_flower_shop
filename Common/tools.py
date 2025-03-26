from datetime import datetime, timedelta


def is_within_24_hours(delivery_date):
    current_time = datetime.now()
    time_difference = delivery_date - current_time
    return time_difference <= timedelta(hours=24) and time_difference >= timedelta(0)
