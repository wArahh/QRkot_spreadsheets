from datetime import timedelta


def format_duration(delta: timedelta) -> str:
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    day_label = "day" if days == 1 else "days"
    return (
        f"{days} "
        f"{day_label} "
        f"{hours}"
        f":{minutes}"
        f":{seconds}"
        f".{milliseconds}"
    )
